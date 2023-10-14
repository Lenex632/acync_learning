import threading
from threading import Timer, Thread
from typing import Callable

result = False


def callback_handler(task: Callable = None, args=(), callback_task: Callable = None) -> None:
    global result
    t = 1
    thr = threading.Thread(target=task, args=args, daemon=True)
    timer = threading.Timer(interval=t, function=callback_task)

    thr.start()
    timer.start()

    thr.join(t + 0.1)
    timer.cancel()

    timer.join()
