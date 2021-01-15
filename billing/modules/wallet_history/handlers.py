from billing.modules.db_helpers.get import get_all_by_col_value
from billing.models import wallet_history_table
from billing.app import app


async def get_all_wallet_history_by_wallet_id(wallet_id: int):
    async with app.db.acquire() as conn:
        return await get_all_by_col_value(wallet_history_table, conn, "wallet_id", wallet_id)
