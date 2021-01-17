from typing import Optional
from aiopg.sa import SAConnection
from psycopg2.errors import LockNotAvailable
from billing.modules.wallet.exceptions import (
    OperationUnavailableException,
    WalletNotFoundException,
)
from billing.schemas import WalletCreate, Wallet, WalletUpdate, WalletHistoryCreate
from billing.models import wallet_table
from billing.modules.db_helpers.get import (
    get_by_id,
    get_by_id_with_lock,
    get_by_col_value,
)
from billing.modules.wallet_history.crud import create_wallet_history
from billing.modules.db_helpers.create import create
from billing.modules.db_helpers.update import update_by_id


async def get_wallet_by_id(conn: SAConnection, wallet_id: int) -> Optional[Wallet]:
    wallet = await get_by_id(wallet_table, conn, wallet_id)
    if wallet:
        return Wallet(**wallet)
    return None


async def get_wallet_by_user_id(conn: SAConnection, user_id: int) -> Optional[Wallet]:
    wallet = await get_by_col_value(wallet_table, conn, "user_id", user_id)
    if wallet:
        return Wallet(**wallet)
    return None


async def create_wallet(conn: SAConnection, wallet_data: WalletCreate) -> Wallet:
    async with conn.begin():
        wallet = await create(wallet_table, conn, wallet_data.dict())
        return Wallet(**wallet)


async def update_wallet(
    conn: SAConnection, wallet: Wallet, data_for_update: WalletUpdate
) -> Wallet:
    async with conn.begin():
        updated_wallet = await update_by_id(wallet_table, conn, wallet.id, data_for_update.dict())
        updated_wallet = Wallet(**updated_wallet)
        wallet_history_data = WalletHistoryCreate(
            wallet_id=wallet.id,
            old_balance=wallet.balance,
            new_balance=updated_wallet and updated_wallet.balance,
        )
        await create_wallet_history(conn, wallet_history_data)
        return updated_wallet


async def get_wallet_with_lock(conn: SAConnection, wallet_id: int) -> Wallet:
    async with conn.begin():
        try:
            wallet = await get_by_id_with_lock(wallet_table, conn, wallet_id)
        except LockNotAvailable:
            raise OperationUnavailableException
        if not wallet:
            raise WalletNotFoundException(wallet_id=wallet_id)
        return Wallet(**wallet)
