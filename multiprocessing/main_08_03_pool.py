from multiprocessing import Pool, current_process
from time import sleep


def task(x):
    print(current_process().name, current_process().pid)
    sleep(2)
    return x*x


def initial(data):
    pr = current_process()
    print(f"Инициализация при старте {pr.name}, pid={pr.pid} c аргументом {data}")


if __name__ == '__main__':
    with Pool(5, maxtasksperchild=1, initializer=initial, initargs=("info",)) as pool:
        print(pool.map(task, [1, 2, 3, 4, 5, 6, 7, 8, 9])) # [1, 4, 9, 16, 25, 36, 49, 64, 81]