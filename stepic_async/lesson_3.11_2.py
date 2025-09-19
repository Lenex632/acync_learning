import asyncio


async def wait_tasks(tasks: list[asyncio.Task], timeout: float | int) -> tuple[dict, set]:
    done_dict = {}
    done, not_done = await asyncio.wait(tasks, timeout=timeout)
    for task in done:
        name = task.get_name()
        try:
            done_dict[name] = task.result()
        except asyncio.CancelledError:
            done_dict[name] = 'Cancelled'
        except Exception as e:
            done_dict[name] = e

    return done_dict, set(not_done)

