import asyncio
from time import perf_counter

type T = dict[str, list]

start = perf_counter()


async def scrap() -> T:
    while perf_counter() - start < 3:
        return {}
    return {'new': ["товар№1", "товар№2", "товар№3", "товар№4", "товар№5"]}


async def spider(item) -> None:
    print(f'{item} is caught')


# Your code
event = asyncio.Event()
queue = asyncio.Queue()


async def coro_watcher() -> None:
    while True:
        await asyncio.sleep(0.1)
        products = await scrap()
        products = products.get("new")
        if products is not None:
            event.set()
            for p in products:
                queue.put_nowait(p)
            break


async def coro_handler() -> None:
    await event.wait()
    product = await queue.get()
    await spider(product)


async def main_logic() -> None:
    handler_tasks = [coro_handler() for _ in range(5)]
    await asyncio.gather(coro_watcher(), *handler_tasks)


if __name__ == '__main__':
    asyncio.run(main_logic())

