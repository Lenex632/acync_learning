import asyncio
from typing import Callable


async def sleep_with_callback(delay, func: Callable = None):
    await asyncio.sleep(delay)
    if func is not None:
        return func()
    return None

