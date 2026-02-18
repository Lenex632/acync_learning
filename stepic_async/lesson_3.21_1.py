import asyncio


async def get_data():
    pass


async def get_request():
    pass


async def get_another_job():
    pass


semaphore = asyncio.Semaphore(2)


async def semaphored_coro():
    if semaphore.locked():
        await get_another_job()
    else:
        async with semaphore:
            await get_data()
            await get_request()

