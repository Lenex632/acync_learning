import asyncio
import types


@types.coroutine
def switch_task():
    yield


async def coroutine_1():
    print("1")
    await switch_task()  # <- !
    print("2")


async def coroutine_2():
    print("A")
    await switch_task()  # <- !
    print("B")


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(coroutine_1())
        tg.create_task(coroutine_2())


if __name__ == '__main__':
    import time
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}")
