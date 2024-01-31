import time


def task(a, b, c):
    if not isinstance(a , int | float):
        raise TypeError("not a number!")
    time.sleep(a/10)
    return sum((a, b, c))


def data_gen():
    yield 1, 2, 3
    yield 10, 20, 30
    yield "a", "b", "c"
    yield 1.0, 2.0, 3.0


from multiprocessing.pool import Pool


if __name__ == '__main__':
    with Pool() as pool:
        result = []
        process = [pool.apply_async(task, i) for i in data_gen()]
        for i in process:
            try:
                result.append(i.get())
            except Exception as error:
                result.append(error)

        print(result)  # [6, 60, TypeError('not a number!'), 6.0]
