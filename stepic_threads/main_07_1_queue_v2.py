import threading
import queue
from time import sleep

queue = queue.PriorityQueue(60)
account = 0


def producer(t: int | float, file: str) -> None:
    with open(file) as file:
        for line in file:
            priority, amount, assignment = line.split()
            queue.put((int(priority), int(amount), assignment))
            print(f'{threading.current_thread().name}\tput\t->\t({line.strip()})\tQueue size = {queue.qsize()}')
            sleep(t)


def consumer(t: int | float) -> None:
    global account
    while True:
        payment = queue.get()
        priority, amount, assignment = payment
        print(f'{threading.current_thread().name}\t<-\tget{payment}\tQueue size = {queue.qsize()}')
        sleep(t)
        if assignment == 'receipt':
            account += amount
        else:
            account -= amount
        queue.task_done()


if __name__ == '__main__':
    threads = [
        threading.Thread(target=producer, args=(0, "files/payment_orders_1.txt"), name="producer_1"),
        threading.Thread(target=producer, args=(0, "files/payment_orders_2.txt"), name="producer_2"),
        threading.Thread(target=consumer, args=(0, ), name="consumer_1", daemon=True),
        threading.Thread(target=consumer, args=(0, ), name="consumer_2", daemon=True),
        threading.Thread(target=consumer, args=(0, ), name="consumer_3", daemon=True)
    ]
    [thread.start() for thread in threads]

    [threads[i].join() for i in range(2)]
    queue.join()

    print(f"{account=}")
    print("END MAIN")
