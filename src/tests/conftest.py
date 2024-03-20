import asyncio
from typing import List

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import create_app
from src.models import Link
from src.schemas.links import Entry
from src.services.links import LinkService
from src.utils.unitofwork import UnitOfWork


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture
async def unit_of_work() -> UnitOfWork:
    return UnitOfWork()


@pytest_asyncio.fixture
async def add_links_to_db(unit_of_work: UnitOfWork):
    async def wrapper(links: Entry) -> List[Link]:
        added_links = await LinkService().add_links(
            links=links, uow=unit_of_work
        )
        return added_links

    return wrapper


@pytest_asyncio.fixture
async def delete_links(unit_of_work: UnitOfWork):
    async def wrapper(links: Entry):
        return await LinkService().delete_links(links=links, uow=unit_of_work)

    return wrapper


@pytest_asyncio.fixture
async def links(add_links_to_db, delete_links):
    links = Entry(
        links=[
            "https://github.com/ser-guzun/",
        ]
    )
    added_links = await add_links_to_db(links=links)
    yield added_links
    await delete_links(links=links)
