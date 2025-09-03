from multiprocessing import Process, Lock
from time import sleep


def print_n(lock: Lock, n: int) -> None:
    with lock:
        print('Первый раз', n)
        sleep(0.1)
        print('Второй раз', n)


if __name__ == '__main__':
    lock = Lock()
    for n in range(10):
        Process(target=print_n, args=(lock, n)).start()
