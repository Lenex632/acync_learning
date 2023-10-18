import threading
from time import sleep
from random import randint


barrier = threading.Barrier(4)  # объект барьера для 4 участников


def multi_stage_task():
    sleep(randint(0, 4))  # эмуляция работы первого этапа
    print(f"{threading.current_thread().name} stage 1")
    barrier.wait()  # ожидаем завершения работы первого этапа всех участников

    sleep(randint(0, 4))  # эмуляция работы второго этапа
    print(f"{threading.current_thread().name} stage 2")
    barrier.wait()  # ожидаем завершения работы второго этапа всех участников

    print("all threads finished stages")  # выводим на печать после того, как все участники прошли барьер 2-го этапа


if __name__ == '__main__':
    thr = [threading.Thread(target=multi_stage_task) for _ in range(4)]
    [t.start() for t in thr]
