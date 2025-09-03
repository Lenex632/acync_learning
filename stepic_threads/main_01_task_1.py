import threading
import time


def user_interface():
    while True:
        time.sleep(0.2)
        print('-', end='')


def task():
    while True:
        time.sleep(0.61)
        print('*', end='')


if __name__ == '__main__':
    th1 = threading.Thread(target=user_interface, name='th1')
    th2 = threading.Thread(target=task, name='th2')

    th1.start()
    th2.start()
