import threading
import time
from typing import Callable


class HubHendler:
    def __init__(self, n: int, task: Callable, n_threads: int):
        self.n = n
        self.task = task
        self.n_threads = n_threads
        self.sema = threading.Semaphore(self.n)

    def start_hub(self):
        tasks = [threading.Thread(target=self.pull_to_sema) for _ in range(self.n_threads)]
        [t.start() for t in tasks]
        [t.join() for t in tasks]

    def pull_to_sema(self):
        with self.sema:
            self.task()
            time.sleep(1)


def do_something():
    print('something')


if __name__ == '__main__':
    hub = HubHendler(4, do_something, 10)
    hub.start_hub()
    print('END')
