from billing.modules.db_helpers.exceptions import CreateEntityException
from typing import Any, Dict
from aiopg.sa import SAConnection
from .execute import get_one


async def create(table, conn: SAConnection, data: dict) -> Dict[Any, Any]:
    query = table.insert().values(**data).returning(*table.c)
    entity = await get_one(conn, query)
    if entity is None:
        raise CreateEntityException
    return entity
