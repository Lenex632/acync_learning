import asyncio
from time import perf_counter


class AsyncSimpleIterator:
    def __init__(self, n: int = 0):
        self.n = n
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        self.count += 1
        if self.count > self.n:
            raise StopAsyncIteration
        await asyncio.sleep(self.count, self.count)
        return self.count


async def main():
    async for elem in AsyncSimpleIterator(3):
        print(elem)


if __name__ == '__main__':
    start_time = perf_counter()
    asyncio.run(main())
    print(f"All done in {perf_counter() - start_time:.2f}c.")

