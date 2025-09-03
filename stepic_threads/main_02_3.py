import threading
import time


def task(func, t, s):
    func(t)
    print(f"task done! #{s}")


if __name__ == '__main__':
    threads = []
    for i in range(20):
        threads.append(threading.Thread(target=task, args=(time.sleep, 1, i)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
