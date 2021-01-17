from aiopg.sa import SAConnection
from billing.modules.db_helpers.get import get_all_by_col_value
from billing.modules.db_helpers.create import create
from billing.models import wallet_history_table
from billing.schemas import WalletHistoryCreate


async def create_wallet_history(conn: SAConnection, wallet_history_data: WalletHistoryCreate):
    await create(wallet_history_table, conn, wallet_history_data.dict())


async def get_all_wallet_history_by_wallet_id(conn: SAConnection, wallet_id: int):
    return await get_all_by_col_value(wallet_history_table, conn, "wallet_id", wallet_id)
