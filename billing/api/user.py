from billing.modules.user.exceptions import UserAlreadyExistsException
from fastapi import APIRouter
from billing.modules.user.handlers import create_user_with_wallet
from billing.schemas import UserWithWallet, UserCreate
from fastapi import HTTPException

user_router = APIRouter()


@user_router.post("", response_model=UserWithWallet, status_code=201)
async def create_user(user_data: UserCreate):
    try:
        return await create_user_with_wallet(user_data=user_data)
    except UserAlreadyExistsException:
        raise HTTPException(status_code=400, detail="User with such email already exists")
