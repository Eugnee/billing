import asyncio
from billing.schemas import Wallet


def get_slow_coro_mock(return_value=None):
    def wrapper():
        async def sleep(*a, **kw):
            await asyncio.sleep(1)
            return return_value

        return sleep

    return wrapper


def wallet_mock(data=None):
    wallet_data = {
        "id": 1,
        "balance": 500,
        "user_id": 1,
    }
    if data:
        wallet_data.update(data)
    return Wallet(**wallet_data)
