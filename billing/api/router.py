from billing.config import settings
from fastapi import APIRouter
from .user import user_router
from .wallet import wallet_router

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(user_router, prefix="/users")
router.include_router(wallet_router, prefix="/wallets")
