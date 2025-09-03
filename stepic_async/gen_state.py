import inspect
import threading
import time


def g_task():
    for i in range(2):
        time.sleep(1)  # <-!
        yield i


g = g_task()


def print_state() -> None:
    while True:
        print(inspect.getgeneratorstate(g))
        time.sleep(0.5)


threading.Thread(target=print_state).start()
next(g)
next(g)

