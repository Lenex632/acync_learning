import queue
import threading


def get_obj():
    for i in range(6):
        yield i


def is_prim(obj):
    return obj % 2 == 0


def task():
    while True:
        obj = main_q.get()
        if is_prim(obj):
            prim_queue.put(obj)
        else:
            sub_queue.put(obj)


def main():
    for i in get_obj():
        if i is None:
            break
        else:
            main_q.put(i)


if __name__ == '__main__':
    main_q = queue.Queue()
    prim_queue = queue.Queue()
    sub_queue = queue.Queue()

    main_thr = threading.Thread(target=main)
    thr_1 = threading.Thread(target=task, daemon=True)
    thr_2 = threading.Thread(target=task, daemon=True)

    main_thr.start()
    thr_1.start()
    thr_2.start()

    main_thr.join()
    thr_1.join(0.2)
    thr_2.join(0.2)
