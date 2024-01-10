import multiprocessing
import time
from random import randint

sources = ["2023_08.csv", "2023_07.csv", "2023_06.csv", "2023_05.csv", "2023_04.csv"]


def handler(file: str) -> None:
    """
    Функция обработки платежей
    """
    i = randint(0, 3)
    time.sleep(i)
    print(file, i)


def main(t: int | float):
    prs = [multiprocessing.Process(target=handler, args=(source, ), daemon=True) for source in sources]
    [pr.start() for pr in prs]
    time.sleep(t)
    [pr.terminate() for pr in prs]
    [pr.join() for pr in prs]
    [pr.close() for pr in prs]


if __name__ == '__main__':
    main(1)
