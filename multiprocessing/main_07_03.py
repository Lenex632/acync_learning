import multiprocessing
from multiprocessing import Process, Lock, SimpleQueue

lock = Lock()
data = SimpleQueue()


def handler(elem):
    return elem


def worker(lock: Lock, stor: SimpleQueue) -> None:
    # функция - обертка для синхронизированного доступа к элементам очереди, обработки и записи
    # результата обратно в очередь
    while True:
        with lock:
            elem = stor.get()
            if elem is not None:
                elem = handler(elem)
                stor.put(elem)
            else:
                break


if __name__ == '__main__':
    pass
