from multiprocessing import Process, Pipe


def child_function(conn):
    with conn:
        data = conn.recv()  # Получение данных из родительского процесса
        result = data + ' 1'
        #  Какая-то работа с данными, получение result
        conn.send(result)  # Отправка результата обратно в родительский процес


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()

    child_process = Process(target=child_function, args=(child_conn,))
    child_process.start()

    with parent_conn:
        parent_conn.send("Данные для дочернего процесса")
        # Получение ответа от дочернего процесса через объект connection
        response = parent_conn.recv()
    print("Ответ от дочернего процесса:", response)

    child_process.join()
