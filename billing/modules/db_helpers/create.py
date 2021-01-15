from typing import Any, Dict, Optional
from aiopg.sa import SAConnection
from .execute import get_one


async def create(table, conn: SAConnection, data: dict) -> Optional[Dict[Any, Any]]:
    query = table.insert().values(**data).returning(*table.c)
    return await get_one(conn, query)
