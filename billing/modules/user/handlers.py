from billing.modules.user.crud import create_user, get_user_by_email
from billing.modules.user.exceptions import UserAlreadyExistsException
from billing.modules.wallet.crud import create_wallet
from billing.schemas import UserCreate, WalletCreate, UserWithWallet
from billing.app import app


async def create_user_with_wallet(user_data: UserCreate) -> UserWithWallet:
    async with app.db.acquire() as conn:
        user = await get_user_by_email(conn, email=user_data.email)
        if user:
            raise UserAlreadyExistsException
        async with conn.begin():
            try:
                user = await create_user(conn, user_data)
            except UserAlreadyExistsException:
                raise
            wallet = await create_wallet(conn, WalletCreate(user_id=user.id))
        return UserWithWallet(**user.dict(), balance=wallet.balance, wallet_id=wallet.id)
