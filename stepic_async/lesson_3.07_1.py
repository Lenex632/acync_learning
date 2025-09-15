import asyncio


coroutines = []


async def main():
    return await asyncio.gather(*coroutines, return_exceptions=True)


if __name__ == '__main__':
    results = asyncio.run(main())

