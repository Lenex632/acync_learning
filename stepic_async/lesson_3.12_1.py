import asyncio


async def main(coroutines) -> list[str]:
    tasks = []
    for coro in coroutines:
        if coro.__name__ == 'response_limit':
            limit = asyncio.create_task(coro)
        else:
            tasks.append(asyncio.create_task(coro))

    try:
        async with asyncio.timeout(None) as atm:
            res = await limit
            atm.reschedule(asyncio.get_running_loop().time() + res)
            await asyncio.sleep(res)
    except TimeoutError:
        pass

    results = [task.get_coro().__name__ for task in tasks if not task.cancel()]
    return results

