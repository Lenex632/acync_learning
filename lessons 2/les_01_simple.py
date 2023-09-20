import asyncio
import time


async def count():
    print('one')
    await asyncio.sleep(1)
    print('two')


async def main():
    await asyncio.gather(count(), count(), count())


if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter() - start
    print(f"{__file__} executed in {end:0.2f} seconds.")

# def main():
#     for _ in range(3):
#         count()
#
# if __name__ == "__main__":
#     s = time.perf_counter()
#     main()
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
