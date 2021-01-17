from billing.schemas.wallet import WalletReplenisment
from billing.modules.wallet.handlers import replenish_wallet
from billing.schemas.user import UserCreate
from billing.modules.user.handlers import create_user_with_wallet
from faker import Faker

fake = Faker()


async def create_new_user_with_wallet():
    user_data = UserCreate(
        email=fake.email(),
        name=fake.name(),
    )
    return await create_user_with_wallet(user_data=user_data)


async def replenish_wallet_with_500_cents(wallet_id: int):
    wallet_replenishment = WalletReplenisment(cents=500)
    await replenish_wallet(wallet_id=wallet_id, wallet_replenishment=wallet_replenishment)
