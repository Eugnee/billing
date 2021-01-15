from aiopg.sa import SAConnection
from .execute import get_one


async def create(table, conn: SAConnection, data: dict) -> dict:
    query = table.insert().values(**data).returning(*table.c)
    return await get_one(conn, query)
