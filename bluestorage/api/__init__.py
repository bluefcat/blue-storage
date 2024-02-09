from bluestorage.setting import setting
from bluestorage.databases.query import Query


async def get_query() -> Query:
    return await Query.setup(setting["DB"]["url"])
