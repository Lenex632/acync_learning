import threading
import time

_bl, _tm, _vl = True, 0, 4


def task(sema: threading.Semaphore, text):
    s = sema.acquire(blocking=_bl, timeout=_tm)
    print(f"thread id = {threading.current_thread().ident} print {text}, acquire={s}, value= {sema._value}")
    time.sleep(1)
    sema.release()
    # with sema:
    #     print(f"thread id = {threading.current_thread().ident} print {text}, acquire={sema}, value= {sema._value}")
    #     time.sleep(1)


if __name__ == '__main__':
    semaphore = threading.Semaphore(_vl)

    thr = []
    for i in range(20):
        thr.append(threading.Thread(target=task, args=(semaphore, i)))
    for t in thr:
        t.start()

    for t in thr:
        t.join()

    print(semaphore._value)

