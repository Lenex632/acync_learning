import asyncio
from typing import Callable


# Напишите класс асинхронного обработчика заданий с ограничением по количеству одновременных выполнений:
#     Атрибуты создания:
#     limit: int — максимально разрешенное количество одновременных выполнений;
#     coro_function — функция-корутина (не использует аргументов). Функция используется для создания нескольких экземпляров-корутин, которых будут "одновременно" выполнять несколько задач;
#     n_tasks: int — общее количество выполняющих корутин задач.
#     В классе кроме инициализатора должен быть публичный метод coroutine start_hub() вызываемый без аргументов. Он создает и запускает указанное количество задач (n_tasks) для выполнения корутин с учетом ограничения по количеству одновременных выполнений (limit).
#     При необходимости дополнительно можно создавать и использовать другие методы.
#     Решите задачу используя семафор.


class AsyncHubHandler:
    def __init__(self, limit: int, coro_function: Callable, n_tasks: int):
        self.n_tasks = n_tasks
        self.coro_function = coro_function
        self.sema = asyncio.Semaphore(limit)

    async def start_task(self, coro: Callable):
        async with self.sema:
            await coro()

    async def start_hub(self):
        tasks = [self.start_task(self.coro_function) for _ in range(self.n_tasks)]
        await asyncio.gather(*tasks)

