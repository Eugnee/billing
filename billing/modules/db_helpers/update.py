from billing.modules.db_helpers.exceptions import UpdateEntityException
from typing import Any, Dict
from aiopg.sa import SAConnection
from .execute import get_one


async def update_by_id(table, conn: SAConnection, row_id: int, data: dict) -> Dict[Any, Any]:
    query = table.update().values(**data).where(table.c.id == row_id).returning(*table.c)
    entity = await get_one(conn, query)
    if entity is None:
        raise UpdateEntityException
    return entity
