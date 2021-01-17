from .crud import get_all_wallet_history_by_wallet_id
from billing.app import app


async def get_last_wallet_history_by_wallet_id(wallet_id: int):
    async with app.db.acquire() as conn:
        wallet_history = await get_all_wallet_history_by_wallet_id(conn, wallet_id=wallet_id)
        if wallet_history:
            return sorted(wallet_history, key=lambda x: x["created_at"], reverse=True)[0]
