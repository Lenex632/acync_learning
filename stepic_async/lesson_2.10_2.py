import socket
import select
from collections import deque  # если Вы будете делать tasks, используя очередь, а не список


def server() -> None:
    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        yield "accept", server_sock
        conn, addr = server_sock.accept()
        tasks.append(client(conn))


def client(client_sock: socket.socket) -> None:
    while True:
        yield "recv", client_sock
        data = client_sock.recv(1024)
        try:
            numbers = [int(n) for n in data.decode().split()]
            res = sum(numbers)
        except Exception as er:
            msg = repr(er)
        else:
            msg = f'{"+".join(map(str, numbers))}={res}'
        finally:
            yield "send", client_sock
            client_sock.send(msg.encode())


tasks = deque((server(), ))


def event_loop():
    for_read, for_write = {}, {}
    while True:
        if not tasks:
            sockets_for_read, sockets_for_write, _ = select.select(for_read, for_write, [], 2)
            if not sockets_for_read and not sockets_for_write:
                print("Нет новых запросов за отведенный таймаут, завершаем event_loop")
                break
            for sock in sockets_for_read:
                tasks.append(for_read.pop(sock))
            for sock in sockets_for_write:
                tasks.append(for_write.pop(sock))

        task = tasks.popleft()
        try:
            method, conn = next(task)
            if method == "send":
                for_write[conn] = task
            else:
                for_read[conn] = task
        except socket.error:
            print("Потеря связи с клиентом")

