from typing import Optional, Sequence

from sqlalchemy import select

from bluestorage.databases import Database
from bluestorage.databases.schema import ItemInfo 

class ItemInfoRepository:
    """
    ItemInfo's repository
    Create, Update, Read, Delete a ItemInfo
    """

    def __init__(self, database: Database) -> None:
        self.Session = database.session_maker
    
    async def create(self, fileinfo: ItemInfo) -> None:
        async with self.Session.begin() as session:
            return session.add(fileinfo)

    async def update(self, new_fileinfo: ItemInfo) -> None:
        async with self.Session.begin() as session:
            fileinfo = await session.get(ItemInfo, new_fileinfo.id)
            
            assert fileinfo
            fileinfo.name = new_fileinfo.name        
            fileinfo.path = new_fileinfo.path        

    async def read(self, id: str) -> Optional[ItemInfo]:
        async with self.Session.begin() as session:
            return await session.get(
                ItemInfo,
                id,
            )

    async def delete(self, fileinfo: ItemInfo) -> None:
        async with self.Session.begin() as session:
            await session.delete(fileinfo)

    async def read_all(self) -> Sequence[ItemInfo]:
        async with self.Session.begin() as session:
            smst = select(ItemInfo)

            result = await session.execute(smst)
            return result.scalars().all()

