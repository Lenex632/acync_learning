import socket
import time
import multiprocessing


def server() -> None:
    server_sock = socket.socket()
    address = ("localhost", 5555)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(address)
    server_sock.listen()
    while True:
        conn, addr = server_sock.accept()
        print(f"Connection from {addr}")
        while data := conn.recv(1024):
            print(f"received data {data}")
            try:
                numbers = [int(n) for n in data.decode().split()]
                res = sum(numbers)
            except Exception as er:
                msg = repr(er)
            else:
                msg = f'{"+".join(map(str, numbers))}={res}'
            finally:
                conn.send(msg.encode())


def client() -> None:
    client_sock = socket.socket()
    address = ("localhost", 5555)
    time.sleep(1)
    client_sock.connect(address)
    client_sock.send('1 2 3'.encode())
    response = client_sock.recv(1024)
    print(f"Response from server: {response.decode()}")
    client_sock.send('2 2 2'.encode())
    response = client_sock.recv(1024)
    print(f"Response from server: {response.decode()}")
    client_sock.send('3 3 3'.encode())
    response = client_sock.recv(1024)
    print(f"Response from server: {response.decode()}")
    client_sock.close()


def main() -> None:
    pr_server = multiprocessing.Process(target=server)
    pr_server.start()

    pr_client1 = multiprocessing.Process(target=client)
    pr_client1.start()
    pr_client2 = multiprocessing.Process(target=client)
    pr_client2.start()

    pr_server.join()
    pr_client1.join()
    pr_client2.join()


if __name__ == "__main__":
    main()

