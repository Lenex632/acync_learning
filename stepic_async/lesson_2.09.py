import multiprocessing
import random
import time
import socket
import selectors
from typing import Tuple, Any


def create_server(address: Tuple[str, int]) -> socket.socket:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen()
    return server_socket


def handler(data: bytes) -> bytes:
    try:
        # print(f"received data {data}")
        numbers = [int(n) for n in data.decode().split()]
        res = sum(numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        return msg.encode()


def accept_conn(server_sock: socket.socket, sel: selectors.BaseSelector) -> None:
    try:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        sel.register(conn, selectors.EVENT_READ, send_response)
    except socket.error as e:
        print(f"Error accepting connection: {e}")


def send_response(client_sock: socket.socket, *args: Any) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, selectors.EVENT_READ, accept_conn)
        while True:
            for k, _ in sel.select():
                sock: socket.socket = k.fileobj
                try:
                    k.data(sock, sel)
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    sock.close()
                    sel.unregister(sock)


def client() -> None:
    client_sock = socket.socket()
    time.sleep(1)
    address = ("localhost", 5555)
    client_sock.connect(address)
    for i in range(3):
        msg = [str(random.randint(1, 100)) for _ in range(5)]
        client_sock.send(' '.join(msg).encode())
        response = client_sock.recv(1024)
        print(f"{i} Response from server: {response.decode()}")
    client_sock.close()


def server() -> None:
    address = ("localhost", 5555)
    server_socket = create_server(address)
    event_loop(server_socket)


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
    # server()

