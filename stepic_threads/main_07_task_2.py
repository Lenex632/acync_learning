import threading
import queue
from datetime import datetime

from main_07_task_1 import CCD


obj = [1, 2, 3, 4, 5]
t_wait = 1


def get_next_declar():
    for i in obj:
        yield i


def handler(el):
    pass


main_queue = queue.PriorityQueue(30)
sup_queue = queue.Queue()


def producer():
    for el in get_next_declar():
        if el is None:
            break
        if main_queue.full():
            sup_queue.put(CCD(el))
        else:
            main_queue.put(CCD(el))


def consumer():
    while True:
        el = main_queue.get()
        handler(el)
        main_queue.task_done()


if __name__ == '__main__':
    prod_0 = threading.Thread(target=producer)

    prod_0.start()
    [threading.Thread(target=consumer, name=f'insp_{i}', daemon=True).start() for i in range(1, 4)]

    prod_0.join()
    main_queue.join()

    while not sup_queue.empty():
        main_queue.put(sup_queue.get())


def consumer_v2(t_wait):

    while True:
        try:
            el = main_queue.get(timeout=t_wait)
        except queue.Empty:
            print(f'Empty {datetime.now()} thread = {threading.current_thread().name}')
            break
        print(el.id)


def main():
    threading.Thread(target=consumer_v2, name='insp_1', args=(t_wait, ), daemon=True).start()
