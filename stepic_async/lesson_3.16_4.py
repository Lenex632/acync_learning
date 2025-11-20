import time
import asyncio
from contextlib import asynccontextmanager
from concurrent.futures import Executor


@asynccontextmanager
async def thread_executor(n_threads: int):
    pool = Executor(max_workers=n_threads)
    try:
        yield pool
    finally:
        await pool.shutdown(wait=False)


n: int = 2


async def coro():
    await asyncio.sleep(0.5)
    return 1


def functi():
    print(123)
    time.sleep(2)
    return 2


entities = [coro(), coro(), functi, coro(), functi]


def cb(task: asyncio.Task | asyncio.Future):
    print(task)
    if not task.cancelled():
        try:
            print(task.result())
        except Exception as exc:
            print(f"Ошибка: {exc!r}")


async def main():
    loop = asyncio.get_running_loop()
    try:
        async with asyncio.TaskGroup() as tg, Executor(n) as thread_pool:
            for task in entities:
                if asyncio.iscoroutine(task):
                    tg.create_task(task).add_done_callback(cb)
                else:
                    loop.run_in_executor(thread_pool, task).add_done_callback(cb)
    except ExceptionGroup:
        pass


if __name__ == '__main__':
    asyncio.run(main())

