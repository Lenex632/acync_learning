import asyncio
from itertools import count
import time

_count = count(1)


async def my_coro():
    n = next(_count)
    result = await asyncio.sleep(n, n)
    print(f"{result=}")
    return result


def callback_task(args):
    print(f"Вызван коллбэк с аргументом {args}")


async def main():
    task_1 = asyncio.create_task(my_coro())
    print(task_1)
    task_2 = asyncio.create_task(my_coro())
    await task_2


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"all done in {time.perf_counter() - start_time:.2f}")

