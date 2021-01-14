from typing import Optional
from aiopg.sa import SAConnection


async def get_one(conn: SAConnection, query) -> Optional[dict]:
    result = await conn.execute(query)
    row = await result.first()
    return dict(row) if row else row
