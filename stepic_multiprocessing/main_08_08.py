import time


def task(arg):
    time.sleep(arg / 3)
    return arg + arg


from multiprocessing.pool import Pool
from typing import Iterable, Callable


def main(func: Callable, iterable: Iterable, timeout: int) -> list:
    with Pool() as pool:
        process = [pool.apply_async(func, (i, )) for i in iterable]
        result = []
        time.sleep(timeout)
        for pr in process:
            if pr.ready():
                result.append(pr.get())
            else:
                result.append('TimeoutError')
    return result


if __name__ == '__main__':
    data = (1, 2, 12, 1)
    print(main(task, data, 1))  # [2, 4, 'TimeoutError', 2]
