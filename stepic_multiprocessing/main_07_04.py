import time
from multiprocessing import Process, Queue, Semaphore


def handler(elem):
    return elem


def worker(elem_queue: Queue, result_queue: Queue, sema: Semaphore) -> None:
    while True:
        with sema:
            elem = elem_queue.get()
            if elem is not None:
                print(elem)
                result_queue.put(handler(elem))
            else:
                break


if __name__ == "__main__":
    elem_queue = Queue()
    result_queue = Queue()
    obj_lock = Semaphore(value=3)

    [elem_queue.put(i) for i in range(5)]
    elem_queue.put(None)

    pr = Process(target=worker, args=(elem_queue, result_queue, obj_lock))
    pr.start()

    while True:
        try:
            print(result_queue.get(block=True, timeout=1))
        except:
            break