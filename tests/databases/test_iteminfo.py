import pytest

from bluestorage.util import get_hash 
from bluestorage.databases.query import Query
from bluestorage.databases.schema import ItemInfo

@pytest.mark.asyncio
async def test_iteminfo_read(query: Query):
    fileinfo = await query.iteminfo.read(get_hash("test1.out"))
    assert fileinfo
    assert fileinfo.id == get_hash("test1.out")
    assert fileinfo.name == "test1.out"
    assert fileinfo.path == "./storage/test1.out"

    fileinfo = await query.iteminfo.read(get_hash("test2.out"))
    assert fileinfo
    assert fileinfo.id == get_hash("test2.out")
    assert fileinfo.name == "test2.out"
    assert fileinfo.path == "./storage/test2.out"

@pytest.mark.asyncio
async def test_iteminfo_update(query: Query):
    fileinfo = await query.iteminfo.read(get_hash("test1.out"))
    assert fileinfo
    
    fileinfo.name = "test.in"
    await query.iteminfo.update(fileinfo)

    fileinfo = await query.iteminfo.read(get_hash("test1.out"))
    assert fileinfo

    assert fileinfo.name == "test.in"

@pytest.mark.asyncio
async def test_iteminfo_delete(query: Query):
    fileinfo = await query.iteminfo.read(get_hash("test1.out"))
    assert fileinfo
    assert fileinfo

    await query.iteminfo.delete(fileinfo)
    assert not await query.iteminfo.read(get_hash("test1.out"))

