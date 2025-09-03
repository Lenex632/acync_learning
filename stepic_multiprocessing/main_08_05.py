from multiprocessing.pool import Pool


def data_gen():
    for i in range(1, 4):
        yield 1 * i, 2 * i, 3 * i


def task(a, b, c):
    return a, b, c


if __name__ == "__main__":
    with Pool() as pool:
        results = pool.starmap(func=task, iterable=data_gen())
        print(results)
