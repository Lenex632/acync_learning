import multiprocessing
from typing import Any
from time import sleep, perf_counter
from multiprocessing import Queue


def task(elem: Any) -> None:
    print(f"id={multiprocessing.current_process().ident}, {elem}")
    sleep(0.1)


def run(task: callable, count: int, queue: Queue):
    for i in range(count):
        if not queue.empty():
            task(queue.get())


def pool(max_workers: int = None, task: callable = None, args: tuple | list = None) -> None:
    max_workers = max_workers or multiprocessing.cpu_count()

    n = len(args) // max_workers
    m = len(args) % max_workers
    queue = Queue()
    for arg in args:
        queue.put(arg)

    for i in range(m):
        pr = multiprocessing.Process(target=run, args=(task, n + 1, queue))
        pr.start()
        pr.join()

    for i in range(max_workers - m):
        pr = multiprocessing.Process(target=run, args=(task, n, queue))
        pr.start()
        pr.join()


if __name__ == "__main__":
    # start_time = perf_counter()
    # for i in range(10):
    #     task(i)
    # print(perf_counter() - start_time)  # ~1 с.
    #
    # start_time = perf_counter()
    # for i in range(10):
    #     pr = multiprocessing.Process(target=task, args=(i, ))
    #     pr.start()
    #     pr.join()
    # print(perf_counter() - start_time)  # ~2 с.

    args = [1, 2, 3, 4, 5, 6, 7]
    pool(max_workers=3, task=task, args=args)
