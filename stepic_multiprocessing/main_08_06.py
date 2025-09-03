from multiprocessing.pool import Pool


def data_gen():
    for i in range(1, 4):
        yield i


def task(a):
    if a == 2:
        raise ValueError
    else:
        return a


def handler(arg):
    print('success')


def err_handler(arg):
    print('error', arg)


if __name__ == "__main__":
    with Pool() as pool:
        res = pool.map_async(func=task, iterable=data_gen())
        try:
            res.get()
            handler(res)
        except Exception as e:
            err_handler(e)
