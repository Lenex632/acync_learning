import socket
import select
import time
import multiprocessing
import random

from collections import deque


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        yield "accept", server_sock
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        tasks.append(client(conn))


def client(client_sock: socket.socket) -> None:
    while True:
        yield "recv", client_sock
        data = client_sock.recv(1024)
        # print(f"received data {data}")
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


def event_loop():
    for_read, for_write = {}, {}
    while True:
        if not tasks:
            sockets_for_read, sockets_for_write, _ = select.select(for_read, for_write, [])
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
        except socket.error as e:
            print(e)


def main_client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    time.sleep(1)
    client_sock.connect(address)
    for i in range(3):
        msg = [str(random.randint(1, 100)) for _ in range(5)]
        client_sock.send(' '.join(msg).encode())
        time.sleep(.5)
        response = client_sock.recv(1024)
        print(f"{i} Response from server: {response.decode()}")
    client_sock.close()


def main_server() -> None:
    event_loop()


tasks = deque((server(), ))


def main() -> None:
    pr_server = multiprocessing.Process(target=main_server)
    pr_server.start()

    clients = []
    for _ in range(3):
        pr_client = multiprocessing.Process(target=main_client)
        pr_client.start()
        clients.append(pr_client)

    pr_server.join(5)
    for c in clients:
        c.join()
    pr_server.terminate()
    pr_server.kill()


if __name__ == "__main__":
    main()
    # main_server()

