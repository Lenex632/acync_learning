import time
from random import randint

import multiprocessing
from threading import Thread


class ParallelExecuter(multiprocessing.Process):
    def __init__(self, tasks: list[callable] | tuple[callable], args: list | tuple, timeout: int | float = None):
        super().__init__()
        self.tasks = tasks
        self.args = args
        self.timeout = timeout

        self.log: list[str] = []
        self.processes: list[tuple[multiprocessing.Process, str]] = []

    def execute(self):
        thread = Thread(target=self.create_processes)
        thread.start()
        thread.join(self.timeout)

        for pr, task_name in self.processes:
            if pr.is_alive():
                pr.terminate()
                pr.join()
                pr.close()
                self.log.append(f'{task_name} processing timeout exceeded')
            else:
                self.log.append(f'{task_name} completed successfully')

    def create_processes(self):
        ctx = multiprocessing.get_context()
        for task, arg in zip(self.tasks, self.args):
            pr = ctx.Process(target=task, args=arg, daemon=True)
            self.processes.append((pr, task.__name__))
            pr.start()
        for pr, name in self.processes:
            pr.join()


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


if __name__ == '__main__':
    tasks = [task1, task2, task3, task4]
    source = [[1], [2], [3], [4]]
    executor = ParallelExecuter(tasks, source, 2)
    executor.execute()
    print(executor.log)
