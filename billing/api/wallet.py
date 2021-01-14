from billing.modules.wallet.exceptions import (
    IdenticalWalletsException,
    InsufficientFundsException,
    OperationUnavailableException,
    WalletNotFoundException,
)
from billing.modules.wallet.handlers import replenish_wallet, transfer_money_from_one_to_another
from billing.schemas import Wallet, WalletReplenisment, WalletsList
from fastapi import APIRouter, HTTPException

wallet_router = APIRouter()


@wallet_router.post("/{wallet_id}/replenish", response_model=Wallet)
async def wallet_replenishment(wallet_id: int, wallet_replenishment: WalletReplenisment):
    try:
        return await replenish_wallet(
            wallet_id=wallet_id, wallet_replenishment=wallet_replenishment
        )
    except WalletNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Wallet with id={e.wallet_id} not found")
    except OperationUnavailableException:
        raise HTTPException(status_code=429, detail="Cant replenish wallet now, try it later")


@wallet_router.post("/{from_wallet_id}/transfer_to/{to_wallet_id}", response_model=WalletsList)
async def transfer_money(
    from_wallet_id: int, to_wallet_id: int, wallet_replenishment: WalletReplenisment
):
    try:
        return await transfer_money_from_one_to_another(
            from_wallet_id=from_wallet_id,
            to_wallet_id=to_wallet_id,
            wallet_replenishment=wallet_replenishment,
        )
    except WalletNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"Wallet with id={e.wallet_id} not found")
    except OperationUnavailableException:
        raise HTTPException(status_code=429, detail="Cant replenish wallet now, try it later")
    except InsufficientFundsException as e:
        raise HTTPException(status_code=400, detail=f"Insufficient funds on wallet {e.wallet_id}")
    except IdenticalWalletsException:
        raise HTTPException(status_code=400, detail="Wrong request")
