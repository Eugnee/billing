from typing import Any, Optional
from aiopg.sa import SAConnection
from sqlalchemy.sql import Select
from .execute import get_one, get_all


def get_select_by_col_name_query(table, col_name: str, col_value: Any) -> Select:
    return table.select().where(getattr(table.c, col_name) == col_value)


async def get_by_col_value(
    table, conn: SAConnection, col_name: str, col_value: Any
) -> Optional[dict]:
    query = get_select_by_col_name_query(table, col_name=col_name, col_value=col_value)
    return await get_one(conn, query)


async def get_all_by_col_value(
    table, conn: SAConnection, col_name: str, col_value: Any
) -> Optional[dict]:
    query = get_select_by_col_name_query(table, col_name=col_name, col_value=col_value)
    return await get_all(conn, query)


async def get_by_id(table, conn: SAConnection, row_id: int) -> Optional[dict]:
    return await get_by_col_value(table, conn, "id", row_id)


async def get_by_id_with_lock(table, conn: SAConnection, row_id) -> Optional[dict]:
    query = get_select_by_col_name_query(table, "id", row_id)
    query = query.with_for_update(
        read=False, nowait=True, of=None, skip_locked=False, key_share=False
    )
    return await get_one(conn, query)
