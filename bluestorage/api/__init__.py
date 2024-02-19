from fastapi import FastAPI

from bluestorage.setting import setting
from bluestorage.databases.query import Query

class BlueAPI(FastAPI):
    def __init__(self, db_url: str, *args, **kwargs):
        self.db_url = db_url
        self.query = None 
        super().__init__(*args, **kwargs)

    async def get_query(self) -> Query:
        if not self.query:
            self.query = await Query.setup(self.db_url)
        return self.query

app = BlueAPI(setting["DB"]["url"])

