import asyncio

sources = ["https://yandex.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru",
           "https://яndex.ru",
           "https://www.youtube.com",
           "https://www.porshe.de",
           "https://www.whatsapp.com",
           "https://www.baidu.com"]


async def get_status(url: str) -> tuple[str, str]:
    _, host = url.rsplit("//")
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, 443, ssl=True), timeout=3)
        query = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"\r\n"
        )
        writer.write(query.encode())
        await writer.drain()

        data = await reader.readline()
        data = data.decode().strip()
        print(url, data)
        writer.close()
        await writer.wait_closed()
    except asyncio.exceptions.TimeoutError:
        print(url, 'Слишком большое время ожидания')
    except Exception as e:
        print(url, repr(e))


async def main() -> None:
    tasks = [get_status(source) for source in sources]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

