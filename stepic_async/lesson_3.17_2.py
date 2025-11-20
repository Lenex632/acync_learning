import random
import asyncio


class AsyncRandomIntegerIterator:
    def __init__(self, min_value: int, max_value: int, count: int):
        self.min_value = min_value
        self.max_value = max_value
        self.count = count
        self.current = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.current >= self.count:
            raise StopAsyncIteration
        await asyncio.sleep(0)  # для возможности кооперативного выполнения запланированных задач
        self.current += 1
        return random.randint(self.min_value, self.max_value)


async def main():
    a = AsyncRandomIntegerIterator(1, 5, 10)

    async for i in a:
        print(i, sep=' ')


if __name__ == "__main__":
    asyncio.run(main())

