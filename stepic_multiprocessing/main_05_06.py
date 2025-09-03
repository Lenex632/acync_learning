import time
from random import uniform


def get_files():
    for file in ["logo.png", "bar.png", "phon.png", "box.png", "info.png", "front_logo.png"]:
        print('put')
        time.sleep(uniform(0.1, 0.5))
        yield file
    time.sleep(1)


def image_processing(file: str) -> str:
    print(file)
    time.sleep(uniform(0.5, 0.7))  # эмуляция работы
    return f"{file} processed successfully"


from multiprocessing import JoinableQueue, SimpleQueue, Process


def producer(queue: JoinableQueue):
    for file in get_files():
        queue.put(file)


def consumer(queue: JoinableQueue, log_queue: SimpleQueue):
    while True:
        file = queue.get()
        res = image_processing(file)
        log_queue.put(res)
        queue.task_done()


if __name__ == '__main__':
    log_queue = SimpleQueue()
    queue = JoinableQueue()

    prod = Process(target=producer, args=(queue, ))
    prod.start()

    consumers = [Process(target=consumer, args=(queue, log_queue), daemon=True) for _ in range(3)]
    for pr in consumers:
        pr.start()

    prod.join()
    queue.join()

    log_processing = []
    while not log_queue.empty():
        log_processing.append(log_queue.get())

    print(log_processing)
