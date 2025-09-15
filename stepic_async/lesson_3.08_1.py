import asyncio
import random
import time


cashed_data = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}


async def get_request(n: int):
    await asyncio.sleep(0, n)


async def get_data(n: int):
    if n in cashed_data:
        return cashed_data[n]
    return await get_request(n)


async def main():
    async with asyncio.TaskGroup() as tg:
        for _ in range(50_000):
            i = random.randint(1, 10)
            tg.create_task(get_data(i))


start_time = time.perf_counter()

if __name__ == '__main__':

    # asyncio.run(main())  # <-!

    loop = asyncio.new_event_loop()
    loop.set_task_factory(asyncio.eager_task_factory)  # <-!
    loop.run_until_complete(main())

    print(f"Время выполнения программы: {time.perf_counter() - start_time:.3f}c.")

