from fastapi import FastAPI

from bluestorage.setting import setting
from bluestorage.databases.query import Query

class BlueAPI(FastAPI):
    def __init__(self, db_url: str, *args, **kwargs):
        self.db_url = db_url
        super().__init__(*args, **kwargs)

    async def get_query(self) -> Query:
        return await Query.setup(self.db_url)

app = BlueAPI(setting["DB"]["url"])

