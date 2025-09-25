import asyncio
from concurrent.futures import ProcessPoolExecutor


async def main():
    tasks = []
    coros = [coro for coro in entities if asyncio.iscoroutine(coro)]
    funcs = [func for func in entities if not asyncio.iscoroutine(func)]

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=len(funcs)) as executor:
        for coro in coros:
            tasks.append(asyncio.create_task(coro))
        for func in funcs:
            tasks.append(loop.run_in_executor(executor, func))
        for task in asyncio.as_completed(tasks):
            await task


if __name__ == '__main__':
    asyncio.run(main())

