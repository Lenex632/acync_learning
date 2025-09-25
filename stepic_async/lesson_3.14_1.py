import asyncio


def some_func():
    import time
    time.sleep(1)
    ...


async def some_core():
    await asyncio.sleep(2)
    ...


entities = [some_core(), some_func]


async def main():
    tasks = []
    for entity in entities:
        if asyncio.iscoroutine(entity):
            tasks.append(asyncio.create_task(entity))
        else:
            tasks.append(asyncio.create_task(asyncio.to_thread(entity)))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

