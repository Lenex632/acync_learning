import asyncio


async def main(coroutine):
    task = asyncio.create_task(coroutine)
    limit = await asyncio.create_task(response_limit)

    try:
        result = await asyncio.wait_for(task, limit)
    except TimeoutError:
        print('Задача отменена, превышено время ожидания!')
        result = None

    return result

