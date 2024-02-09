from typing import Any, Optional

from bluestorage.databases import Database
from bluestorage.databases.repository import (
    ItemInfoRepository,
    UserRepository,
    TokenRepository,
)

class Query(object):
    """
    Query is singleton
    """
    def __init__(self, database: Optional[Database] = None) -> None:
        cls = type(self)
        if not hasattr(cls, "database"):
            if not database:
                return
            self.database: Database = database
    
    def __new__(cls, *args: Any, **kwargs: Any) -> "Query":
        if not hasattr(cls, "instance"):
            cls.instance = super(Query, cls).__new__(cls)

        return cls.instance
    
    @classmethod
    async def setup(cls, url: str, **kwargs: Any) -> "Query":
        return cls(await Database.setup(url, **kwargs))

    @property
    def iteminfo(self) -> ItemInfoRepository:
        return ItemInfoRepository(self.database)

    @property
    def user(self) -> UserRepository:
        return UserRepository(self.database)

    @property
    def token(self) -> TokenRepository:
        return TokenRepository(self.database)
