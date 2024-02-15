import pytest

from sqlalchemy.exc import IntegrityError

from bluestorage.util import get_hash 
from bluestorage.databases.query import Query
from bluestorage.databases.schema import User

@pytest.mark.asyncio
async def test_user_create(query: Query):
    try:
        user = await query.user.create(
            User(
                id=get_hash("testuser"), 
                username="testuser", 
                password="it is new user"
            )
        )
        assert False
    except IntegrityError:
        assert True

@pytest.mark.asyncio
async def test_user_read(query: Query):
    user = await query.user.read(get_hash("testuser"))
    assert user 
    assert user.id == get_hash("testuser")
    assert user.username == "testuser" 
    assert user.password != "testpassword" 
    
    user = await query.user.read(get_hash("nothing"))
    assert not user

@pytest.mark.asyncio
async def test_user_read_username(query: Query):
    user = await query.user.read_username("testuser")
    assert user
    
    user = await query.user.read_username("nothing")
    assert not user

@pytest.mark.asyncio
async def test_user_update(query: Query):
    user = await query.user.read_username("testuser")
    assert user 
    
    password = user.password
    user.password = "new_password"
    await query.user.update(user)

    user = await query.user.read_username("testuser")
    assert user 
    assert user.password != "new_password"
    assert user.password != password

@pytest.mark.asyncio
async def test_user_delete(query: Query):
    user = await query.user.read_username("testuser")
    assert user 

    await query.user.delete(user)
    assert not await query.user.read_username("testuser")

