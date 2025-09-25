import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial


def cb(task: asyncio.Task | asyncio.Future, task_type: str) -> None:
    try:
        result = task.result()
    except BaseException as e:
        result = repr(e)
    finally:
        print(f'{task_type} завершена с результатом {result}')


async def main():
    loop = asyncio.get_running_loop()
    tasks = []
    coros = []
    io_funcs = []
    cpu_funcs = []
    for entity in entities:
        if asyncio.iscoroutine(entity):
            coros.append(entity)
        elif hasattr(entity, 'cpu'):
            cpu_funcs.append(entity)
        else:
            io_funcs.append(entity)

    with ThreadPoolExecutor(max_workers=len(io_funcs)) as th_pool, ProcessPoolExecutor() as pr_pool:
        for coro in coros:
            task = asyncio.create_task(coro)
            task.add_done_callback(partial(cb, task_type='Корутина'))
            tasks.append(task)
        for io_func in io_funcs:
            task = loop.run_in_executor(th_pool, io_func)
            task.add_done_callback(partial(cb, task_type='Блокирующая задача'))
            tasks.append(task)
        for cpu_func in cpu_funcs:
            task = loop.run_in_executor(pr_pool, cpu_func)
            task.add_done_callback(partial(cb, task_type='Расчетная задача'))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    asyncio.run(main())

