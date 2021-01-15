from typing import Optional
from aiopg.sa import SAConnection


async def get_one(conn: SAConnection, query) -> Optional[dict]:
    result = await conn.execute(query)
    row = await result.first()
    return dict(row) if row else row


async def get_all(conn: SAConnection, query) -> Optional[dict]:
    result = await conn.execute(query)
    rows = await result.fetchall()
    return [dict(row) for row in rows]
