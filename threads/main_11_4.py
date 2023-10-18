import concurrent.futures
import time


def slow_square(x):
    time.sleep(x)
    return x**2


def main_1():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(slow_square, i) for i in (3, 1, 4, 2)]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


def main_2():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(slow_square, i) for i in (3, 1, 5)]

    with concurrent.futures.ThreadPoolExecutor() as executor_2:
        futures_2 = [executor_2.submit(slow_square, i) for i in (4, 2, 6)]

        for future in concurrent.futures.as_completed(futures+futures_2):
            print(future.result())


if __name__ == '__main__':
    main_2()
