import asyncio
import inspect
from typing import Coroutine, Iterable


class ForCompletedIterator:
    def __init__(self, coroutines: list[Coroutine]):
        self.todo = {asyncio.create_task(coro) for coro in coroutines}
        self.done = asyncio.Queue()
        for coro in self.todo:
            coro.add_done_callback(self.handle_callback)

    def handle_callback(self, task: asyncio.Task):
        self.done.put_nowait(task)
        self.todo.remove(task)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self.todo:
            raise StopAsyncIteration
        item = await self.done.get()
        return item


def async_for_completed(aws: list[Coroutine]):
    if not isinstance(aws, Iterable):
        raise TypeError("Должен быть передан список с объектами корутин")
    for i in aws:
        if not inspect.iscoroutine(i):
            raise TypeError("Должен быть передан список с объектами корутин")
    return ForCompletedIterator(aws)


async def coro():
    await asyncio.sleep(3)
    return "123"


async def main():
    tasks = [coro(), coro(), coro()]
    async for res in async_for_completed(tasks):
        print(f"{res}=")

if __name__ == "__main__":
    asyncio.run(main())

