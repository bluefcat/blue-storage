import asyncio
import anyio
import pytest

from httpx import AsyncClient

@pytest.mark.asyncio
async def test_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_read_items(client: AsyncClient, token: dict):
    authorization = f"{token['token_type']} {token['access_token']}"
    response = await client.get(
        "/items",
        headers= {"accept": "application/json", "Authorization": authorization}
    )

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_upload_items(client: AsyncClient, token: dict):
    authorization = f"{token['token_type']} {token['access_token']}"
    async with await anyio.open_file("./tests/files/dummy_a.txt", "rb") as f:
        response = await client.post(
            "/items",
            headers = {"accept": "application/json", "Authorization": authorization},
            files={"item": ("dummy_a.txt", await f.read())} 
        )
    
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_delete_items(client: AsyncClient, token: dict):
    authorization = f"{token['token_type']} {token['access_token']}"
    async with await anyio.open_file("./tests/files/dummy_a.txt", "rb") as f:
        response = await client.post(
            "/items",
            headers = {"accept": "application/json", "Authorization": authorization},
            files={"item": ("dummy_a.txt", await f.read())} 
        )
    
    assert response.status_code == 201
    id: str = response.json()['id']
    
    response = await client.delete(
        f"/items/{id}",
        headers = {
            "accept": "application/json",
            "Authorization": authorization,
        })
    assert response.status_code == 200


