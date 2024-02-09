import asyncio

from typing import Any 
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from bluestorage.databases.schema import Base

class Database:
    """
    This class make the database, and create engine
    """

    def __init__(self, engine: AsyncEngine) -> None:
        self.__engine = engine

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            self.__engine, class_=AsyncSession, expire_on_commit=False
        )

    @classmethod
    async def setup(cls, url: str, **kwargs: Any) -> "Database":
        engine = create_async_engine(url, **kwargs)
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all, checkfirst=True)
        return cls(engine)

