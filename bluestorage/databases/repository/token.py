from typing import Optional, Sequence

from sqlalchemy import select

from bluestorage.databases import Database
from bluestorage.databases.schema import Token

class TokenRepository:
    """
    Token's repository
    Create, Update, Read, Delete a Token
    """

    def __init__(self, database: Database) -> None:
        self.database = database
    
    async def create(self, token: Token) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            return session.add(token)

    async def update(self, new_token: Token) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            token = await session.get(Token, new_token.id)
            assert token

    async def read(self, user_id: str) -> Optional[Token]:
        Session = self.database.session_maker
        async with Session.begin() as session:
            smst = select(Token).where(Token.user_id == user_id)

            result = await session.execute(smst)
            return result.scalars().first()

    async def delete(self, token: Token) -> None:
        Session = self.database.session_maker
        async with Session.begin() as session:
            await session.delete(token)
    
    async def read_token(self, access_token: str) -> Optional[Token]:
        Session = self.database.session_maker
        async with Session.begin() as session:
            smst = select(Token).where(Token.access_token == access_token)

            result = await session.execute(smst)
            return result.scalars().first()
