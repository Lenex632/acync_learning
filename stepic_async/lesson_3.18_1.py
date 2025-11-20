import asyncio


AsyncQueueType = asyncio.Queue | asyncio.LifoQueue | asyncio.PriorityQueue


async def consumer(queue: AsyncQueueType):
    while True:
        task = asyncio.current_task().get_name()
        try:
            async with asyncio.timeout(.2):
                element = await queue.get()
                print(f'{task} извлек элемент очереди {repr(element)}')
        except TimeoutError:
            print(f'Работа {task} завершена!')
            break

