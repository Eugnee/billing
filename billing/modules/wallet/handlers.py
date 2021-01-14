from typing import List
from aiopg.sa.connection import SAConnection
from psycopg2.errors import LockNotAvailable
from billing.modules.wallet.exceptions import (
    IdenticalWalletsException,
    InsufficientFundsException,
    OperationUnavailableException,
    WalletNotFoundException,
)
from billing.schemas.wallet import WalletReplenisment
from billing.schemas import WalletFields, Wallet, WalletHistoryFields
from billing.app import app
from billing.models import wallet_table, wallet_history_table
from billing.modules.db_helpers.crud import (
    create,
    get_by_id,
    get_by_id_with_lock,
    get_by_col_name,
    update_by_id,
)


async def get_wallet_by_id(wallet_id: int):
    async with app.db.acquire() as conn:
        return await get_by_id(wallet_table, conn, wallet_id)


async def get_wallet_by_user_id(user_id: int):
    async with app.db.acquire() as conn:
        return await get_by_col_name(wallet_table, conn, "user_id", user_id)


async def create_wallet(wallet_fields: WalletFields):
    async with app.db.acquire() as conn:
        async with conn.begin():
            return await create(wallet_table, conn, wallet_fields.dict())


async def update_wallet(conn: SAConnection, wallet: Wallet, new_wallet_fields: WalletFields):
    async with conn.begin():
        updated_wallet = await update_by_id(wallet_table, conn, wallet.id, new_wallet_fields.dict())
        wallet_history_data = WalletHistoryFields(
            wallet_id=wallet.id,
            old_balance=wallet.balance,
            new_balance=updated_wallet["balance"],
        )
        await create(wallet_history_table, conn, wallet_history_data.dict())
        return updated_wallet


async def get_wallet_with_lock(conn: SAConnection, wallet_id: int) -> Wallet:
    try:
        wallet = await get_by_id_with_lock(wallet_table, conn, wallet_id)
    except LockNotAvailable:
        raise OperationUnavailableException
    if not wallet:
        raise WalletNotFoundException(wallet_id=wallet_id)
    return Wallet(**wallet)


async def replenish_wallet(wallet_id: int, wallet_replenishment: WalletReplenisment):
    async with app.db.acquire() as conn:
        async with conn.begin():
            wallet = await get_wallet_with_lock(conn, wallet_id=wallet_id)
            new_wallet_fileds = WalletFields(
                user_id=wallet.user_id, balance=wallet.balance + wallet_replenishment.amount
            )
            return await update_wallet(conn, wallet=wallet, new_wallet_fields=new_wallet_fileds)


async def transfer_money_from_one_to_another(
    from_wallet_id: int, to_wallet_id: int, wallet_replenishment: WalletReplenisment
) -> List[dict]:
    async with app.db.acquire() as conn:
        async with conn.begin():
            if from_wallet_id == to_wallet_id:
                raise IdenticalWalletsException

            from_wallet = await get_wallet_with_lock(conn, from_wallet_id)
            to_wallet = await get_wallet_with_lock(conn, to_wallet_id)

            try:
                new_from_wallet_fileds = WalletFields(
                    user_id=from_wallet.user_id,
                    balance=from_wallet.balance - wallet_replenishment.amount,
                )
            except ValueError:
                raise InsufficientFundsException(wallet_id=from_wallet.id)
            from_wallet = await update_wallet(
                conn, wallet=from_wallet, new_wallet_fields=new_from_wallet_fileds
            )

            try:
                new_to_wallet_fileds = WalletFields(
                    user_id=to_wallet.user_id,
                    balance=to_wallet.balance + wallet_replenishment.amount,
                )
            except ValueError:
                raise InsufficientFundsException(wallet_id=to_wallet.id)
            to_wallet = await update_wallet(
                conn, wallet=to_wallet, new_wallet_fields=new_to_wallet_fileds
            )
            return [from_wallet, to_wallet]
