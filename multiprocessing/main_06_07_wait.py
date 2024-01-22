from time import sleep
import random
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait


def foo(w):
    with w:
        for i in range(random.randint(1, 7)):
            sleep_time = random.uniform(0, 1)
            sleep(sleep_time)
            w.send((i, current_process().name))
            if i == 4:
                print("error", current_process().name)
                break
    print("close", current_process().name)


if __name__ == '__main__':
    readers = []

    for i in range(4):
        r, w = Pipe(duplex=False)
        readers.append(r)
        p = Process(target=foo, args=(w,))
        p.start()
        w.close()

    while readers:
        ready_readers = wait(readers)
        print(len(ready_readers), "----------")
        for r in ready_readers:
            try:
                msg = r.recv()
            except EOFError:
                print(f"{r.fileno()} closed")
                readers.remove(r)
            else:
                print(msg)