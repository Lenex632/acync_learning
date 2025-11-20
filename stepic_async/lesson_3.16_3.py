import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def conn_ssh():
    target = AsyncThrSSH()
    try:
        yield target
    finally:
        await target.close()


class AsyncThrSSH:
    def __init__(self):
        print('init')

    async def connect(self):
        print('connect')

    async def close(self):
        print('close')


async def main():
    async with conn_ssh() as conn:
        await conn.connect()


if __name__ == "__main__":
    asyncio.run(main())
