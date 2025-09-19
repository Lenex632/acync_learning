import asyncio


def cb(task: asyncio.Task) -> None:
    coro_name = task.get_coro().__name__
    try:
        print(f"Задача с корутиной {coro_name} вернула результат {task.result()}")
    except BaseException as e:
        print(f"Задача с корутиной {coro_name} завершилась с исключением {repr(e)}")

