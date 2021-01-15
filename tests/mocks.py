import asyncio


def get_slow_coro_mock():
    async def sleep(*a, **kw):
        await asyncio.sleep(1)

    return sleep
