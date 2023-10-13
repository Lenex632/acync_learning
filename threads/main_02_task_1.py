import requests
from time import perf_counter
import threading


sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]
headers_stor = {}  # Храним здесь заголовки


def task(source):
    start_tmp = perf_counter()
    headers_stor[source] = requests.get(source).headers
    delta = perf_counter() - start_tmp
    print(source, delta)


if __name__ == '__main__':
    start = perf_counter()
    tasks = []
    for source in sources:
        tasks.append(threading.Thread(target=task, args=(source, )))
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()

    print(f"completed in {perf_counter()-start} seconds")  # Считаем общее время выполнения всех запросов
    print(*headers_stor.items(), sep="\n")  # Выводим наши заголовки
