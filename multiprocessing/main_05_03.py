import time
from random import uniform


def get_files():
    for file in ["logo.png", "bar.png", "phon.png", "box.png", "info.png", "front_logo.png"]:
        print('put')
        time.sleep(uniform(0.1, 0.5))
        yield file
    yield None


def image_processing(file: str) -> str:
    print(file)
    time.sleep(uniform(0.5, 0.7))  # эмуляция работы
    return f"{file} processed successfully"


from multiprocessing import Queue, Process, Manager


def producer(queue: Queue):
    for file in get_files():
        queue.put(file)


def consumer(queue: Queue, log_processing: Manager().list):
    while True:
        file = queue.get(True)
        if file is None:
            queue.put(None)
            break
        res = image_processing(file)
        log_processing.append(res)


if __name__ == '__main__':
    log_processing = Manager().list()
    queue = Queue()

    prod = Process(target=producer, args=(queue, ))
    prod.start()

    consumers = [Process(target=consumer, args=(queue, log_processing)) for _ in range(3)]
    for pr in consumers:
        pr.start()
    for pr in consumers:
        pr.join()

    print(log_processing)
