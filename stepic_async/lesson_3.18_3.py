import asyncio


async def json_gen():
    pass


async def registrator():
    pass


def final():
    pass


async def producer(queue: asyncio.Queue):
    async for elem in json_gen():
        await queue.put(elem)
    await queue.join()
    final()


async def consumer(queue: asyncio.Queue):
    while True:
        elem = await queue.get()
        await registrator(elem)
        queue.task_done()


async def producer_consumer(queue: asyncio.Queue):
    prod_task = asyncio.create_task(producer(queue))
    cons_tasks = [asyncio.create_task(consumer(queue)) for _ in range(2)]

    await prod_task
    for ct in cons_tasks:
        ct.cancel()
