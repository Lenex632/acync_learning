import time


def task(i):
    time.sleep(i)
    if i == 1:
        raise ValueError("Ops, ValueError")
    return i


from multiprocessing.pool import Pool


class WaitPool:
    def __init__(self, task: callable, iterable: list | tuple):
        self.task = task
        self.iterable = iterable
        self.processes = []

    def start(self):
        self.processes = [self.pool.apply_async(self.task, (i, )) for i in self.iterable]

    def wait(self) -> tuple:
        done = []
        not_done = []
        for pr in self.processes:
            try:
                if pr.successful():
                    done.append(pr)
                else:
                    not_done.append(pr)
            except:
                not_done.append(pr)
        return done, not_done

    def __enter__(self):
        self.pool = Pool()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.terminate()
        self.pool.join()
        self.pool.close()


if __name__ == "__main__":
    args = (0.5, 1, 1.1, 2.2, 3.3, 1.2, 1.4)

    with WaitPool(task, args) as pool:
        pool.start()
        time.sleep(2)
        done, not_done = pool.wait()

    print(len(done), len(not_done))  # 4, 3

    for d in done:
        print(d.get())
    try:
        not_done[0].get()
    except ValueError as err:
        print(err)
