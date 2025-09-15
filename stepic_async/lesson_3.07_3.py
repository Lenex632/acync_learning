import asyncio


coroutines = []


def cb(task: asyncio.Task):
    if task.cancelled():
        cancelled.append(task.get_coro().__name__)
    else:
        if e := task.exception():
            results.append(e)
        else:
            results.append(task.result())


async def main() -> None:
    try:
        final_task = asyncio.create_task(coroutines.pop())
        final_task.add_done_callback(cb)
        async with asyncio.TaskGroup() as tg:
            for coro in coroutines:
                tg.create_task(coro).add_done_callback(cb)
    except Exception:
        pass
    finally:
        await final_task


if __name__ == '__main__':
    results, cancelled = [], []
    asyncio.run(main())

