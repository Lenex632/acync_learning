import socket
import time
import random


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


if __name__ == "__main__":
    client()
