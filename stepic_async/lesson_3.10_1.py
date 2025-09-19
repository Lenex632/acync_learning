import asyncio


coroutines = []


def cb(task: asyncio.Task) -> None:
    name = f'Task_{task.get_coro().__name__}'
    try:
        all_results[name] = task.result()
    except BaseException as error:
        all_results[name] = error


async def main() -> None:
    tasks = []
    for coro in coroutines:
        task = asyncio.create_task(coro)
        task.add_done_callback(cb)
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    all_results = {}
    asyncio.run(main())
