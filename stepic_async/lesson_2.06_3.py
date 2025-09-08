import socket
from typing import Tuple


def server(address: Tuple[str, int]) -> None:
    ser_soc = socket.socket()
    ser_soc.bind(address)
    ser_soc.listen(1)
    conn, addr = ser_soc.accept()
    data = map(int, conn.recv(1024).decode().split())
    print(sum(data))
    ser_soc.close()

