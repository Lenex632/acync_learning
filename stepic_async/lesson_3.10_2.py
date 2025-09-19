import asyncio


print('WARNING: Критическая нагрузка, текущие задачи группы отменены!')


class AlarmOverheatException(Exception):
    pass


async def main(coroutines):
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(service_diag)
            for coro in coroutines:
                tg.create_task(coro)
    except* AlarmOverheatException:
        print('WARNING: Критическая нагрузка, текущие задачи группы отменены!')
    except* Exception as e:
        print(e)

