import threading
import time


def task(event, timeout):
    print("Начали задачу, но ждем события")
    if event.wait(timeout):
        print("Событие получено, выполняем задачу")
    else:
        print("Событие не получено, выходим по таймауту")


if __name__ == '__main__':
    event = threading.Event()
    for t in (1, 3):
        event.clear()
        thread1 = threading.Thread(target=task, args=(event, 2))
        thread1.start()
        time.sleep(t)
        event.set()
        print("Событие установлено")

    # Начали задачу, но ждем события
    # Событие установлено
    # Событие получено, выполняем задачу
    # Начали задачу, но ждем события
    # Событие не получено, выходим по таймауту
    # Событие установлено
