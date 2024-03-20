from typing import List, Set
from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.models import Link
from src.schemas.links import Entry
from src.utils.unitofwork import UnitOfWork


class LinkService:
    async def get_all_domains(
        self, time_from: int, time_to: int, uow: UnitOfWork
    ) -> Set[str]:
        async with uow:
            if not time_from and not time_to:
                links = await uow.links.find_all()
            else:
                links = await uow.links.find_all_in_time_interval(
                    time_from=time_from, time_to=time_to
                )
            await uow.commit()
            domains = [await self._get_domain(link.name) for link in links]
            return set(domains)

    async def add_links(self, links: Entry, uow: UnitOfWork) -> List[Link]:
        async with uow:
            added_links = []
            for link in links.links:
                domain = await self._get_domain(link)
                added_link = await uow.links.add_one(
                    {
                        "name": link,
                        "domain": domain,
                    }
                )
                await uow.commit()
                added_links.append(added_link)
            return added_links

    async def _get_domain(self, link: str) -> str:
        parsed_url = urlparse(link)
        return parsed_url.netloc

    @staticmethod
    async def delete_links(links: Entry, uow: UnitOfWork):
        async with uow:
            for link in links.links:
                try:
                    link_db = await uow.links.find_one(name=link)
                except NoResultFound:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Link {link} not found",
                    )
                await uow.links.delete(name=link_db.name)
                await uow.commit()
            return f"All links was deleted"
