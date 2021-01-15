from typing import List
from aiopg.sa import SAConnection
from .execute import get_one


async def update_by_id(table, conn: SAConnection, row_id: List[int], data: dict) -> dict:
    query = table.update().values(**data).where(table.c.id == row_id).returning(*table.c)
    return await get_one(conn, query)
