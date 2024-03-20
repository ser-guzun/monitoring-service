from typing import Optional

from fastapi import APIRouter
from sqlalchemy.exc import OperationalError

from src.dependencies.service import UOWDep
from src.schemas.links import Entry
from src.services.links import LinkService

router = APIRouter(
    prefix="",
    tags=["links"],
)


@router.get("/visited_domains")
async def get_all_domains(
    uow: UOWDep,
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
) -> dict:
    try:
        domains = await LinkService().get_all_domains(
            time_from=time_from, time_to=time_to, uow=uow
        )
        return {"domains": domains, "status": "ok"}
    except OperationalError as ex:
        return {"status": ex}


@router.post("/visited_links")
async def add_links(links: Entry, uow: UOWDep):
    try:
        added_links = await LinkService().add_links(links=links, uow=uow)
        return {"links": added_links, "status": "ok"}
    except OperationalError as ex:
        return {"status": ex}
