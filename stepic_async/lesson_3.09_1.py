import asyncio


def cb(task: asyncio.Task) -> None:
    try:
        task.result()
    except Exception:
        pass


async def main():
    task_1 = asyncio.create_task(s())
    task_2 = asyncio.create_task(m())
    task_3 = asyncio.create_task(xl())
    task_2.add_done_collback(cb)
    await task_3


if __name__ == '__main__':
    asyncio.run(main())

