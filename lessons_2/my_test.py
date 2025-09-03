import asyncio
import time

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def flash(id_number: int, frequency: int | float, sleep: int) -> int:
    print(c[id_number + 1] + f"Event #{id_number} starts flashing")
    count = round(sleep // frequency)
    for i in range(count):
        print(c[id_number + 1] + f"**\n"
                                 f"Flash from #{id_number} event. It's his {i + 1} time.")
        await asyncio.sleep(frequency)
    return count


async def event(d: dict) -> None:
    id_number, frequency, sleep = d.values()
    start = time.perf_counter()
    count = await flash(id_number, frequency, sleep)
    end = time.perf_counter() - start
    print(c[id_number + 1] + f'---------->Event #{id_number} stops flashing.'
                             f'           Event completed in {end:0.5f} seconds. Flash flashed {count} times.')


async def main(*args) -> None:
    await asyncio.gather(*(event(i) for i in args))

if __name__ == '__main__':
    items = [
        {'id_number': 0, 'frequency': 1, 'sleep': 15},
        {'id_number': 1, 'frequency': 0.3, 'sleep': 10},
        {'id_number': 2, 'frequency': 2, 'sleep': 12}
    ]

    start = time.perf_counter()
    asyncio.run(main(*items))
    end = time.perf_counter() - start

    print(f'Program completed in {end:0.5f} seconds.')
