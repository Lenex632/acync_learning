import asyncio


async def coro():
    pass


async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(coro())
            tg.create_task(coro())
            raise asyncio.CancelledError("Галя, у нас отмена!")
    except BaseException as error:
        print(err)


if __name__ == "__main__":
    asyncio.run(main())
