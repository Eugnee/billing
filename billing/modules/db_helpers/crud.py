from typing import Any, Optional, List
from aiopg.sa import SAConnection
from sqlalchemy.sql import Select
from .execute import get_one


async def create(table, conn: SAConnection, data: dict) -> dict:
    query = table.insert().values(**data).returning(*table.c)
    return await get_one(conn, query)


async def update_by_id(table, conn: SAConnection, row_id: List[int], data: dict) -> dict:
    query = table.update().values(**data).where(table.c.id == row_id).returning(*table.c)
    return await get_one(conn, query)


def get_select_by_col_name_query(table, col_name: str, col_value: Any) -> Select:
    return table.select().where(getattr(table.c, col_name) == col_value)


async def get_by_col_name(
    table, conn: SAConnection, col_name: str, col_value: Any
) -> Optional[dict]:
    query = table.select().where(getattr(table.c, col_name) == col_value)
    return await get_one(conn, query)


async def get_by_id(table, conn: SAConnection, row_id: int) -> Optional[dict]:
    return await get_by_col_name(table, conn, "id", row_id)


async def get_by_id_with_lock(table, conn: SAConnection, row_id) -> Optional[dict]:
    query = get_select_by_col_name_query(table, "id", row_id)
    query = query.with_for_update(
        read=False, nowait=True, of=None, skip_locked=False, key_share=False
    )
    return await get_one(conn, query)
