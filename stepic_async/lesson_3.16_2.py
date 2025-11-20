import asyncio
import time


class TaskGroupCB:
    def __init__(self, callback) -> None:
        self.callback = callback
        self.tacks = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await asyncio.gather(*self.tacks)
        return True

    def create_task(self, coro, name=None):
        task = asyncio.create_task(coro)
        task.set_name(name)
        self.tacks.append(task)
        task.add_done_callback(self.callback)


async def coro(i):
    return await asyncio.sleep(i / 10, i)


def callback(task: asyncio.Task):
    print(f"Задача {task.get_name()} завершилась успешно с результатом {task.result()}")


async def main():
    async with TaskGroupCB(callback) as tgc:
        for n in range(10):
            tgc.create_task(coro(n), name=f"task#{n}")


if __name__ == '__main__':
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"\nAll done in {time.perf_counter() - start_time:.2f}с.")
