import asyncio
from functools import partial


async def main():
    async with asyncio.TaskGroup() as tg:
        for coro, cb, arg in zip(coroutines, callbacks, arguments):
            task = tg.create_task(coro(arg))
            task.set_name(coro.__name__)
            task.add_done_callback(partial(cb, arg))


if __name__ == '__main__':
    asyncio.run(main())

