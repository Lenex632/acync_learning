from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection


def sender(conn: Connection) -> None:
    message = "Hello from sender!"
    number = 42
    float_number = 3.14159
    data = bytearray(message.encode() + number.to_bytes(4, byteorder='big'))

    with conn:
        conn.send(message)
        conn.send(number)
        conn.send(float_number)
        conn.send_bytes(data)


if __name__ == "__main__":
    recv_conn, send_conn = Pipe(duplex=False)
    Process(target=sender, args=[send_conn]).start()

    recv_data = []
    with recv_conn:
        recv_data.append(recv_conn.recv())
        recv_data.append(recv_conn.recv())
        recv_data.append(recv_conn.recv())
        recv_data.append(recv_conn.recv_bytes())

    print(recv_data)
