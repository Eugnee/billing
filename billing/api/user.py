from fastapi import APIRouter
from billing.modules.user.handlers import get_user_by_email, create_user_with_wallet
from billing.schemas import UserWithWallet, UserFields
from fastapi import HTTPException

user_router = APIRouter()


@user_router.post("", response_model=UserWithWallet)
async def create_user(user_fields: UserFields):
    user = await get_user_by_email(email=user_fields.email)
    if user:
        raise HTTPException(status_code=400, detail="User with such email already exists")
    return await create_user_with_wallet(user_fields=user_fields)
