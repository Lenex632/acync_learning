import threading
from time import sleep
from itertools import count

count = count()


def trace_func(frame, event, arg):
    print(f"{next(count)} executing trace func with {threading.current_thread().name=}")
    print(f"{frame=}\n{event=}\n{arg=}")


def get_inform():
    print(f"{threading.current_thread().name=}")
    print(f"{threading.current_thread().ident=}")
    print(f"{threading.current_thread().native_id=}")
    print(f"{threading.get_ident()=}")
    print(f"{threading.get_native_id()=}")
    print("---------------")
    sleep(2)


if __name__ == '__main__':
    threading.settrace(trace_func)
    # threading.setprofile(trace_func)

    thr = [threading.Thread(target=get_inform) for _ in range(3)]
    [t.start() for t in thr]
    sleep(1)
    print(threading.enumerate())
    for t in threading.enumerate():
        print(f"{t.name=}")
        print(f"{t.ident=}")
        print(f"{t.native_id=}")
