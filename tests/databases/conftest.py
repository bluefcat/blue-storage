import pytest
import pytest_asyncio

from bluestorage.util import get_hash
from bluestorage.databases.query import Query
from bluestorage.databases.schema import Base, ItemInfo, User

@pytest.fixture
def user_one():
    return User(id=get_hash("testuser"), username="testuser", password="testpassword")

@pytest.fixture
def fileinfo_one():
    return ItemInfo(id=get_hash("test1.out"), name="test1.out", path="./storage/test1.out")

@pytest.fixture
def fileinfo_two():
    return ItemInfo(id=get_hash("test2.out"), name="test2.out", path="./storage/test2.out")

@pytest_asyncio.fixture(scope="session")
async def _query():
    # if you want to use sqlite in memory, use this line instead of the next one
    query = await Query.setup("sqlite+aiosqlite:///:memory:")
    return query


@pytest_asyncio.fixture(scope="function")
async def query(
    _query: Query,
    user_one: User,
    fileinfo_one: ItemInfo,
    fileinfo_two: ItemInfo,
):
    async with _query.database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all, checkfirst=True)
    await _query.user.create(user_one)
    await _query.iteminfo.create(fileinfo_one)
    await _query.iteminfo.create(fileinfo_two)

    yield _query

    async with _query.database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
