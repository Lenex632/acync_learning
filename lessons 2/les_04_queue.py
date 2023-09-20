import  asyncio
import itertools
import os
import random
import time


async def make_item(size: int = 5) -> str:
    return os.urandom(size).hex()


async def rand_sleep(caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f'{caller} sleeping for {i} seconds.')
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in itertools.repeat(None, n):
        await rand_sleep(caller=f'Producer {name}')
        i = await make_item()
        t = time.perf_counter()
        await q.put((i, t))
        print(f'Producer {name} added <{i}> to queue.')


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await rand_sleep(caller=f'Consumer {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Consumer {name} got element <{i}> in {now - t:0.5f} seconds.')
        q.task_done()


async def main(n_prod: int, n_con: int) -> None:
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(n_prod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(n_con)]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    random.seed(444)
    start = time.perf_counter()
    asyncio.run(main(5, 10))
    end = time.perf_counter() - start
    print(f'Program completed in {end:0.5f} seconds.')
