import socket
import time
import multiprocessing
import random
import threading


def handler(conn, addr) -> None:
    print(f"Connection from {addr}")
    while data := conn.recv(1024):
        # print(f"received data {data}")
        try:
            numbers = [int(n) for n in data.decode().split()]
            res = sum(numbers)
        except Exception as er:
            msg = repr(er)
        else:
            msg = f'{addr}: {"+".join(map(str, numbers))}={res}'
        finally:
            time.sleep(0.3)
            conn.send(msg.encode())


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()

    connections = []

    for i in range(3):
        conn, addr = server_sock.accept()
        connection = threading.Thread(target=handler, args=(conn, addr))
        connections.append(connection)
        connection.start()

    for c in connections:
        c.join()


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    time.sleep(1)
    client_sock.connect(address)
    for _ in range(3):
        msg = [str(random.randint(1, 100)) for _ in range(5)]
        client_sock.send(' '.join(msg).encode())
        response = client_sock.recv(1024)
        print(f"Response from server: {response.decode()}")
    client_sock.close()


def main() -> None:
    pr_server = multiprocessing.Process(target=server)
    pr_server.start()

    clients = []
    for _ in range(3):
        pr_client = multiprocessing.Process(target=client)
        pr_client.start()
        clients.append(pr_client)

    pr_server.join(5)
    for c in clients:
        c.join()
    pr_server.terminate()
    pr_server.kill()


if __name__ == "__main__":
    main()

