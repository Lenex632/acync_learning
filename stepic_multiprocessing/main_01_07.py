import multiprocessing
import time
from random import randint
import typing
from concurrent.futures import ThreadPoolExecutor


def task1(*args):
    i = randint(0, 4)
    time.sleep(i)
    print(*args, i, 'task1')


def task2(*args):
    i = randint(0, 4)
    time.sleep(i)
    print(*args, i, 'task2')


def task3(*args):
    i = randint(0, 4)
    time.sleep(i)
    print(*args, i, 'task3')


def task4(*args):
    i = randint(0, 4)
    time.sleep(i)
    print(*args, i, 'task4')


def create_pull(request, sources):
    with ThreadPoolExecutor() as executor:
        for task, url in zip(request, sources):
            executor.submit(task, url)


def request_handler(request: list[typing.Callable], sources: list[str], timeout: int | float) -> None:
    pr = multiprocessing.Process(target=create_pull, args=(request, sources, ))
    pr.start()

    pr.join(timeout)
    if pr.is_alive():
        pr.terminate()
        pr.join()
        pr.close()


if __name__ == "__main__":
    tasks = [task1, task2, task3, task4]
    links = ['1', '2', '3', '4']
    timeout = 2

    request_handler(tasks, links, timeout)
