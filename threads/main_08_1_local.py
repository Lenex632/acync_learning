import threading

stor = threading.local()
stor.a = 100


def test():
    try:
        print(f"{threading.current_thread().name}, {stor.a=}")
    except AttributeError as err:
        print(f"{threading.current_thread().name} {err}")


if __name__ == '__main__':
    thr_1 = threading.Thread(target=test, name="T1")
    thr_2 = threading.Thread(target=test, name="T2")
    thr_1.start()
    thr_2.start()
    print(f"{threading.current_thread().name}, {stor.a=}")
