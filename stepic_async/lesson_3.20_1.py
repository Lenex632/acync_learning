import asyncio


async def json_gen():
    item = iter(range(1, 11))
    while True:
        try:
            yield next(item)
        except StopIteration:
            break


async def registrator(elem: int) -> None:
    await asyncio.sleep(0)
    print(f'{elem} зарегистрирован для дальнейшей обработки')


def final() -> None:
    print('Final')


event = asyncio.Event()


async def producer(queue: asyncio.LifoQueue) -> None:
    async for elem in json_gen():
        await queue.put(elem)
    event.set()
    await queue.join()
    final()


async def consumer(queue: asyncio.LifoQueue) -> None:
    while not (event.is_set() and queue.empty()):
        elem = await queue.get()
        await registrator(elem)
        queue.task_done()


async def producer_consumer(queue: asyncio.LifoQueue) -> None:
    await asyncio.gather(producer(queue), consumer(queue), consumer(queue))


if __name__ == '__main__':
    queue: asyncio.LifoQueue = asyncio.LifoQueue()
    asyncio.run(producer_consumer(queue))
    print('End')

