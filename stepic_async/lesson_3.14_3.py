import asyncio
from concurrent.futures import ThreadPoolExecutor


async def main():
    coros = [coro for coro in entities if asyncio.iscoroutine(coro)]
    funcs = [func for func in entities if not asyncio.iscoroutine(func)]

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=len(funcs)) as executor:
        async with asyncio.TaskGroup() as tg:
            for coro in coros:
                tg.create_task(coro)
            for func in funcs:
                loop.run_in_executor(executor, func)


if __name__ == '__main__':
    asyncio.run(main())

