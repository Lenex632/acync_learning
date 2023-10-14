import threading


def executer():
    pass


def logging():
    pass


def test_thread_timer(t_check: int | float):
    thr = threading.Thread(target=executer, name='Thread', daemon=True)
    timer = threading.Timer(interval=t_check, function=logging)
    timer.name = 'Timer'

    thr.start()
    timer.start()

    thr.join(t_check + 0.1)
    timer.cancel()

    timer.join()
