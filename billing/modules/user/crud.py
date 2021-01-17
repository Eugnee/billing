from billing.modules.user.exceptions import UserAlreadyExistsException
from typing import Optional
from billing.schemas.user import UserCreate
from billing.modules.db_helpers.get import get_by_col_value
from billing.modules.db_helpers.create import create
from billing.schemas import User
from aiopg.sa import SAConnection
from psycopg2.errors import UniqueViolation
from billing.models import user_table


async def get_user_by_email(conn: SAConnection, email: str) -> Optional[User]:
    user = await get_by_col_value(user_table, conn, "email", email)
    if user:
        return User(**user)
    # explicit because of mypy
    return None


async def create_user(conn: SAConnection, user_data: UserCreate) -> User:
    try:
        user = await create(user_table, conn, user_data.dict())
    except UniqueViolation:
        raise UserAlreadyExistsException
    return User(**user)
