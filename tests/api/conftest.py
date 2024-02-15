import pytest
import pytest_asyncio

from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from bluestorage.setting import setting
from bluestorage.api import BlueAPI 
from bluestorage.api.api import api_router
from bluestorage.api.auth import auth_router

from bluestorage.databases.schema import Base, User


@pytest.fixture(scope="session")
def application():
    app = BlueAPI("sqlite+aiosqlite:///:memory:")
    app.include_router(api_router)
    app.include_router(auth_router)

    return app

@pytest_asyncio.fixture(scope="session")
async def _client(application: BlueAPI):
    async with LifespanManager(application):
        async with AsyncClient(app=application, base_url="http://test") as client:
            yield client

@pytest_asyncio.fixture(scope="function")
async def client(application: BlueAPI, _client: AsyncClient):
    query = await application.get_query()

    async with query.database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all, checkfirst=True)

    yield _client
    
    async with query.database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def token(_client: AsyncClient):
    await _client.post("/signup?username=testuser&password=testpassword")
    
    token = await _client.post("/signin", data={
        "username": "testuser",
        "password": "testpassword"
    })
    return token.json()

