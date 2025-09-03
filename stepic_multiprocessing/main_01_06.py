import multiprocessing
from threading import Timer
import time
from random import randint


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


def stop_prs(prs: list):
    for pr in prs:
        if pr.is_alive():
            pr.terminate()
            pr.join()
            pr.close()


def parallel_handler(tasks: tuple | list, args: tuple | list, timeout: int | float | None = None):
    prs = []
    for i, task in enumerate(tasks):
        prs.append(multiprocessing.Process(target=task, args=(args[i], ), daemon=True))

    [pr.start() for pr in prs]

    if timeout is not None:
        timer = Timer(timeout, function=stop_prs, args=(prs, ))
        timer.start()


if __name__ == "__main__":
    parallel_handler((task1, task2, task3, task4), ((1.5, 1), (1.6, 2), (3, "BFG", "DOOM"), (4, 4, 4.01, 0.9)), timeout=2)
