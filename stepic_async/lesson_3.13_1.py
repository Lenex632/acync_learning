import asyncio


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = await reader.read(1024)
    data = data.decode()
    nums = data.split()
    res = 1
    for num in nums:
        res *= int(num)
    writer.write(f'{"*".join(nums)}={res}'.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main(address: tuple) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        await server.serve_forever()
