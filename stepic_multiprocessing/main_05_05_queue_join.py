import time
import multiprocessing
import random


my_queue = multiprocessing.JoinableQueue()


def produce(q: multiprocessing.JoinableQueue) -> None:
    for i in range(1, 11):
        time.sleep(random.uniform(0, 1))
        q.put(i)  # наполняем очередь цифрами [1, 10] с паузами в пределах секунды


def task(q: multiprocessing.JoinableQueue) -> None:
    while True:
        i = q.get()  # получаем из очереди
        time.sleep(random.uniform(0.5, 2))  # эмулируем работу
        print(f"{i}X{i}={i**2}")  # печатаем результат умножения
        q.task_done()  # отмечаем выполненную задачу с этим элементом


if __name__ == "__main__":
    producer = multiprocessing.Process(target=produce, args=(my_queue, ))
    producer.start()
    workers = [multiprocessing.Process(target=task, args=(my_queue, ), daemon=True) for _ in range(4)]
    for p in workers:
        p.start()
    producer.join()
    my_queue.join()
