# импортируйте необходимое
import asyncio


async def main():
    cors = [my_coroutine_1, my_coroutine_2, my_coroutine_3, my_coroutine_4, my_coroutine_5, my_coroutine_6]
    async with asyncio.TaskGroup() as tg:
        for task in cors:
            tg.create_task(task())


if __name__ == '__main__':
    # напишите решение
    asyncio.run(main())

