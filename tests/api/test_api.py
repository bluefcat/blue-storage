import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running"}

@pytest.mark.asyncio
async def test_read_items_no_auth(client:  AsyncClient):
    response = await client.get("/items")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_upload_item_no_auth(client:  AsyncClient):
    response = await client.post("/items")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_read_item_no_auth(client:  AsyncClient):
    response = await client.get("/items/5")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_item_no_auth(client:   AsyncClient):
    response = await client.delete("/items/5")
    assert response.status_code == 401

