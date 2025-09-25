import asyncio
import time


async def coro():
    await asyncio.sleep(0)


def func():
    time.sleep(0)


async def main():
    start_time = time.perf_counter()
    # Выполните кооперативно 1000 задач с корутиной coro
    async with asyncio.TaskGroup() as tg:
        for i in range(1000):
            tg.create_task(coro())

    print(f"test#1 coro, all done in {time.perf_counter() - start_time:.2f}")

    start_time = time.perf_counter()
    # Выполните 1000 задач с функцией func при помощи asyncio.to_thread
    async with asyncio.TaskGroup() as tg:
        for i in range(1000):
            tg.create_task(asyncio.to_thread(func))

    print(f"test#2 threads, all done in {time.perf_counter() - start_time:.2f}")


if __name__ == '__main__':
    asyncio.run(main())

