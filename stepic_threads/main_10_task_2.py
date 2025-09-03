import threading

from time import sleep


def task_st_1():
    sleep(1)
    print(f'{threading.current_thread().name} - stage_1 pass')


def task_st_2():
    sleep(1)
    print(f'{threading.current_thread().name} - stage_2 pass')


def finalizer():
    print(f'{threading.current_thread().name} - stage done')

# Создайте объект барьера
# Создайте целевую функцию, выполняющую задачи в два этапа
# Создайте и запустите 4 потока


barrier = threading.Barrier(4, action=finalizer)


def task(bar, stage1, stage2):
    stage1()
    bar.wait()
    stage2()


if __name__ == '__main__':
    thrs = [threading.Thread(target=task, args=(barrier, task_st_1, task_st_2)) for _ in range(4)]
    [thr.start() for thr in thrs]
