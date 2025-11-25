import asyncio


class TimeoutLock(asyncio.Lock):
    def __init__(self):
        super().__init__()

    async def acquire(self, timeout: int | float = None):
        if timeout is None:
            result = await super().acquire()
        else:
            try:
                result = await asyncio.wait_for(super().acquire(), timeout=timeout)
            except TimeoutError:
                result = False
        return result


lock = TimeoutLock()


async def coro(timeout: int | float = None):
    await lock.acquire(timeout)
    try:
        await cashed_request()
    finally:
        if lock.locked():
            lock.release()


async def cashed_request():
    pass

