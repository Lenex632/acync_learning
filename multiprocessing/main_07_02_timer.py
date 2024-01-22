from multiprocessing import Process, Event
from time import sleep


class Timer(Process):
    def __init__(self, interval: int | float, function: callable, args: list | tuple, kwargs: dict):
        super().__init__()
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()

    def cancel(self) -> None:
        self.finished.set()

    def run(self) -> None:
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()


def test_task(*args, **kwargs):
    ar = args[0]
    kar = kwargs['0']
    print(f'Hellow from function {ar}_{kar}')


if __name__ == '__main__':
    interval = 1
    args = [(i, ) for i in range(5)]
    kwarg = [{'0': i} for i in range(5)]

    prs = [Timer(interval, test_task, arg, kwarg) for arg, kwarg in zip(args, kwarg)]
    [pr.start() for pr in prs]

    sleep(0.5)
    prs[1].cancel()
    prs[3].cancel()

    [pr.join() for pr in prs]
