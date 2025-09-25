import asyncio
import multiprocessing
from random import randint
# import time


async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        data = await reader.read(1024)
        data = data.decode()
        client_name, n1, n2 = data.split()
        print(f'Получили {n1}, {n2} от {client_name}')
        res = int(n1) + int(n2)
    except Exception as e:
        msg = repr(e)
    else:
        msg = f'{n1}+{n2}={res}'
    finally:
        writer.write(msg.encode())
        await writer.drain()
        print(f'Отправили данные: {msg}')
        writer.close()
        await writer.wait_closed()


async def async_server(address: tuple) -> None:
    server = await asyncio.start_server(handler, *address)
    async with server:
        await server.serve_forever()


def run_async_server() -> None:
    address = ('localhost', 5555)
    asyncio.run(async_server(address))


async def client(address: tuple) -> None:
    name = f'Клиент_№{randint(1, 100)}'
    for i in range(5_000):
        reader, writer = await asyncio.open_connection(*address)  # создаем соединение
        msg = f'{name} {i} {i}'
        writer.write(msg.encode())  # отправляем данные и дожидаемся их отправления
        print(f'{name} отправил: {msg!r}')
        await writer.drain()

        data = await reader.read(1024)  # получаем ответ от сервера
        print(f"{name} получил: {data.decode()!r}")
        writer.close()
        await writer.wait_closed()
        print(f'{name} закрыл соединение')


def run_async_client() -> None:
    asyncio.run(client(('localhost', 5555)))


def main() -> None:
    pr_server = multiprocessing.Process(target=run_async_server)
    pr_server.start()

    clients = []
    for _ in range(3):
        pr_client = multiprocessing.Process(target=run_async_client)
        pr_client.start()
        clients.append(pr_client)

    pr_server.join(5)
    for c in clients:
        c.join()
    pr_server.terminate()
    pr_server.kill()


if __name__ == "__main__":
    main()

