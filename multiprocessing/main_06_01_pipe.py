from multiprocessing import Process, Pipe


def sender(conn):
    conn.send('Hello from sender!')


def receiver(conn):
    data = conn.recv()
    print(f'Received data: {data}')


if __name__ == '__main__':
    # Создаем однонаправленный канал
    # conn1 может использоваться только для приема сообщений,
    # conn2 может использоваться только для отправки сообщений
    recv_conn, send_conn = Pipe(duplex=False)
    # Создаем два процесса участника и передаем им целевые функции
    # передачи и получения сообщения и соответсвующие объекты соединения
    sender_process = Process(target=sender, args=(send_conn,))
    receiver_process = Process(target=receiver, args=(recv_conn,))

    sender_process.start()
    receiver_process.start()

    sender_process.join()
    receiver_process.join()
