import socket
from typing import Tuple


def client(address: Tuple[str, int], msg: str) -> None:
    sk = socket.socket()
    sk.connect(address)
    sk.send(msg.encode())
    sk.close()

