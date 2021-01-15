from billing.modules.user.exceptions import UserAlreadyExistsException
from billing.modules.wallet.handlers import create_wallet
from billing.schemas import UserFields, WalletFields
from billing.app import app
from billing.models import user_table
from billing.modules.db_helpers.create import create
from billing.modules.db_helpers.get import get_by_col_value


async def get_user_by_email(email: str):
    async with app.db.acquire() as conn:
        return await get_by_col_value(user_table, conn, "email", email)


async def create_user_with_wallet(user_fields: UserFields):
    async with app.db.acquire() as conn:
        user = await get_user_by_email(email=user_fields.email)
        if user:
            raise UserAlreadyExistsException
        async with conn.begin():
            user = await create(user_table, conn, user_fields.dict())
        wallet = await create_wallet(WalletFields(user_id=user["id"]))
        return {**user, "balance": wallet["balance"], "wallet_id": wallet["id"]}
