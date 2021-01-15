from typing import Any, Dict, Optional
from aiopg.sa import SAConnection
from .execute import get_one


async def update_by_id(
    table, conn: SAConnection, row_id: int, data: dict
) -> Optional[Dict[Any, Any]]:
    query = table.update().values(**data).where(table.c.id == row_id).returning(*table.c)
    return await get_one(conn, query)
