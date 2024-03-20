from typing import List

import pytest
from httpx import AsyncClient

from src.models.links import Link
from src.schemas.links import Entry


@pytest.mark.asyncio
async def test_add_links(client: AsyncClient, delete_links):
    links = Entry(links=["https://github.com/ser-guzun/"])
    response = await client.post(
        url="http://localhost:8000/visited_links", json=links.dict()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["links"][0]["domain"] == "github.com"
    await delete_links(links=links)


@pytest.mark.asyncio
async def test_get_all_domains(client: AsyncClient, links: List[Link]):
    response = await client.get(url="http://localhost:8000/visited_domains")
    assert response.status_code == 200
    data = response.json()
    assert data["domains"][0] == links[0].domain


@pytest.mark.asyncio
async def test_get_all_domain_inside_time_interval(
    client: AsyncClient, links: List[Link]
):
    url = f"http://localhost:8000/visited_domains?time_from={links[0].created_at}&time_to={links[0].created_at+10}"
    response = await client.get(url=url)
    assert response.status_code == 200
    data = response.json()
    assert data["domains"][0] == links[0].domain
