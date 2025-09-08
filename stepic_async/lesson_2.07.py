import multiprocessing
import socket
import select
import random
import time
from typing import Callable, List, Tuple


def idle_select(sockets: List[socket.socket], idle_handler: Callable, timeout: int | float) -> List[socket.socket]:
    sockets_for_read, _, _ = select.select(sockets, [], [], timeout)
    if not sockets_for_read:
        idle_handler()
        return []
    else:
        return sockets_for_read


def create_server(address: Tuple[str, int]) -> socket.socket:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(address)
    server_socket.listen()
    return server_socket


def handler(data: bytes) -> bytes:
    try:
        numbers = [int(n) for n in data.decode().split()]
        res = sum(numbers)
    except Exception as er:
        msg = repr(er)
    else:
        msg = f'{"+".join(map(str, numbers))}={res}'
    finally:
        return msg.encode()


def accept_conn(server_sock: socket.socket, sockets: List[socket.socket]) -> None:
    try:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        sockets.append(conn)
    except socket.error as error:
        print(f"Error accepting connection: {error}")


def send_response(client_sock: socket.socket) -> None:
    data = client_sock.recv(1024)
    response = handler(data)
    client_sock.send(response)


def event_loop(server_socket: socket.socket) -> None:
    sockets = [server_socket]
    while sockets:
        sockets_for_read, _, _ = select.select(sockets, [], [])
        for sock in sockets_for_read:
            if sock is server_socket:
                accept_conn(sock, sockets)
            else:
                try:
                    send_response(sock)
                except socket.error as error:
                    print(f"Error receiving data: {error}")
                    sock.close()
                    sockets.remove(sock)


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    time.sleep(1)
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
