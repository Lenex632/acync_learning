import asyncio


connection_count = 0


async def server_shutdown(server: asyncio.Server) -> None:
    while True:
        await asyncio.sleep(1)
        if not connection_count:
            server.close()
            await server.wait_closed()


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    global connection_count
    connection_count += 1
    data = await reader.read(1024)
    res = await worker(data.decode())
    writer.write(res.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    connection_count -= 1


async def main(address: tuple) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        asyncio.create_task(server_shutdown(server))
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            print('Работа сервера завершена!')
