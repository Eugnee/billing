from billing.modules.wallet.crud import get_wallet_with_lock, update_wallet
from typing import List
from billing.modules.wallet.exceptions import (
    IdenticalWalletsException,
    InsufficientFundsException,
)
from billing.schemas.wallet import WalletReplenisment
from billing.schemas import WalletUpdate
from billing.app import app


async def replenish_wallet(wallet_id: int, wallet_replenishment: WalletReplenisment):
    async with app.db.acquire() as conn:
        async with conn.begin():
            wallet = await get_wallet_with_lock(conn, wallet_id=wallet_id)
            data_for_update = WalletUpdate(balance=wallet.balance + wallet_replenishment.cents)
            return await update_wallet(conn, wallet=wallet, data_for_update=data_for_update)


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
                new_from_wallet_fileds = WalletUpdate(
                    balance=from_wallet.balance - wallet_replenishment.cents,
                )
            except ValueError:
                raise InsufficientFundsException(wallet_id=from_wallet.id)
            from_wallet = await update_wallet(
                conn, wallet=from_wallet, data_for_update=new_from_wallet_fileds
            )

            try:
                new_to_wallet_fileds = WalletUpdate(
                    balance=to_wallet.balance + wallet_replenishment.cents,
                )
            except ValueError:
                raise InsufficientFundsException(wallet_id=to_wallet.id)
            to_wallet = await update_wallet(
                conn, wallet=to_wallet, data_for_update=new_to_wallet_fileds
            )
            return [from_wallet, to_wallet]
