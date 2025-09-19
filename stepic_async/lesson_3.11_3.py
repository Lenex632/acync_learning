import asyncio


# только допишите функцию main, все остальное, включая ее вызов, сделает тест. система
async def main(aws, *, timeout=None):
    for aw in asyncio.as_completed(aws, timeout=timeout):
        try:
            result = await aw
            print(result)
        except TimeoutError:
            print('Завершение по таймауту')
        except Exception as e:
            print(e)
