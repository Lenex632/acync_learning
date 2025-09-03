import multiprocessing
import time
from random import uniform


class SimplePool:
    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers or multiprocessing.cpu_count()
        self.results = multiprocessing.Queue()
        self.queue = multiprocessing.Queue()

    def run(self, task: callable, count: int, queue: multiprocessing.Queue) -> None:
        for i in range(count):
            if not queue.empty():
                res = task(queue.get())
                self.results.put(res)

    def map(self, task: callable, args: tuple | list) -> tuple | list:
        n = len(args) // self.max_workers
        m = len(args) % self.max_workers
        for arg in args:
            self.queue.put(arg)

        for i in range(m):
            pr = multiprocessing.Process(target=self.run, args=(task, n + 1, self.queue))
            pr.start()
            pr.join()

        for i in range(self.max_workers - m):
            pr = multiprocessing.Process(target=self.run, args=(task, n, self.queue))
            pr.start()
            pr.join()

        res = []
        while not self.results.empty():
            res.append(self.results.get())
        return res


def task(arg):
    time.sleep(uniform(0, 1))
    return multiprocessing.current_process().ident, arg


if __name__ == "__main__":
    args = [1, 2, 3, 4, 5, 6, 7]
    my_pool = SimplePool(3)
    for _id, v in my_pool.map(task=task, args=args):
        print(f"ident={_id}, {v}")