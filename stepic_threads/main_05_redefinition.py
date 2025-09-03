import threading


class TwoTaskThread(threading.Thread):
    def __init__(self, task=None, new_task=None, args=()):
        super().__init__()
        self.task = task
        self.new_task = new_task
        self.args = args

    def run(self) -> None:
        try:
            if self.task is not None:
                self.new_task(self.task(*self.args))
        finally:
            del self.task, self.new_task, self.args


def worker(*args) -> int:
    return sum(args)


def handler(n) -> None:
    print(n)


if __name__ == '__main__':
    my_thread = TwoTaskThread(worker, handler, (1, 2, 3))
    print(my_thread.task)
    print(my_thread.new_task)
    print(my_thread.args)
    my_thread.start()
