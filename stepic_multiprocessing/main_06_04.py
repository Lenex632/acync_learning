from random import choice
from time import sleep


def worker(arr) -> tuple[str, int, float]:
    s = choice((0.1, 1, 0.3, 0.2, 0.1))
    print(f'worker sleep = {s}')
    sleep(s)
    return 'stroka', 1, 3.14


def get_obj():
    for i in range(5):
        yield i


from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection


def child_function(conn: Connection):
    with conn:
        while True:
            recv_obj = conn.recv()
            res = worker(recv_obj)
            conn.send(res)


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    result = []

    child_process = Process(target=child_function, args=(child_conn,), daemon=True)
    child_process.start()

    with parent_conn:
        for obj in get_obj():
            parent_conn.send(obj)

            if parent_conn.poll(0.3):
                recv_data = parent_conn.recv()
                result.append(recv_data)
            else:
                break

    print(result)



