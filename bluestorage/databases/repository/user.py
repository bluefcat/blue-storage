from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from bluestorage.util import get_password_hash
from bluestorage.databases import Database
from bluestorage.databases.schema import User 

class UserRepository:
    """
    User's repository
    Create, Update, Read, Delete a User
    """

    def __init__(self, database: Database) -> None:
        self.database = database
    
    async def create(self, user: User) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            if await self.read_username(user.username):
                raise IntegrityError(statement=None, params=None, orig=BaseException())

            user.password = get_password_hash(user.password)
            return session.add(user)

    async def update(self, new_user: User) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            user = await session.get(User, new_user.id)
            
            assert user
            user.username = new_user.username       
            user.password = get_password_hash(new_user.password)       

    async def read(self, id: str) -> Optional[User]:
        Session = self.database.session_maker
        async with Session.begin() as session:
            return await session.get(
                User,
                id,
            )

    async def delete(self, user: User) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            await session.delete(user)

    async def read_username(self, username: str) -> Optional[User]:
        Session = self.database.session_maker
        async with Session.begin() as session:
            smst = select(User).where(User.username == username)

            result = await session.execute(smst)
            return result.scalars().first()

