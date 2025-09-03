import multiprocessing

def sender(queue):
    message = "Привет, receiver!"
    queue.put(message)

def receiver(queue):
    message = queue.get()
    print("Принято сообщение:", message)


if __name__ == "__main__":
    queue = multiprocessing.Queue()  # Создаем очередь

    sender_process = multiprocessing.Process(target=sender, args=(queue,))
    receiver_process = multiprocessing.Process(target=receiver, args=(queue,))

    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()