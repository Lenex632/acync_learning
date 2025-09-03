import time
from queue import Queue
from threading import Thread

valid_queue = Queue()
none_valid_queue = Queue()


def is_valid(el) -> bool:
    return el % 2 == 0


def handler(elem):
    pass


get_obj = [1, 2, 3, 4, 5, 6, 7]


def main():
    for elem in get_obj:
        if is_valid(elem):
            valid_queue.put(elem)
        else:
            none_valid_queue.put(elem)


def task():
    while True:
        elem = valid_queue.get()
        handler(elem)
        print(elem)


if __name__ == '__main__':
    t1 = Thread(target=task, daemon=True)
    t2 = Thread(target=task, daemon=True)
    t1.start()
    t2.start()

    main_th = Thread(target=main)
    main_th.start()
    main_th.join()
    t1.join(1)
    t2.join(1)
