from billing.modules.wallet_history.handlers import get_all_wallet_history_by_wallet_id
from billing.schemas.wallet import WalletReplenisment
from billing.modules.wallet.handlers import replenish_wallet
from billing.schemas.user import UserFields
from billing.modules.user.handlers import create_user_with_wallet
from faker import Faker

fake = Faker()


async def create_new_user_with_wallet():
    user_fields = UserFields(
        email=fake.email(),
        name=fake.name(),
    )
    return await create_user_with_wallet(user_fields=user_fields)


async def replenish_wallet_with_500_cents(wallet_id: int):
    wallet_replenishment = WalletReplenisment(amount=500)
    await replenish_wallet(wallet_id=wallet_id, wallet_replenishment=wallet_replenishment)


async def get_last_wallet_history_by_wallet_id(wallet_id: int):
    wallet_history = await get_all_wallet_history_by_wallet_id(wallet_id=wallet_id)
    if wallet_history:
        return sorted(wallet_history, key=lambda x: x["created_at"], reverse=True)[0]
