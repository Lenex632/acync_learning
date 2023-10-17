import threading
import time
from random import uniform

lock = threading.Lock()


def test():
    time.sleep(uniform(0, 1))
    lock.acquire(blocking=False)
    print(f"{threading.current_thread().name=}, {lock.locked()=}")


if __name__ == '__main__':
    thr = [threading.Thread(target=test) for _ in range(5)]
    for t in thr:
        t.start()
    for t in thr:
        t.join()

    print(lock.locked())
    print("END")
