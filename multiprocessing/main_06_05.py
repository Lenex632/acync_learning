from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
import struct


def crypter(text: str) -> tuple[str, float]:
    if text == "Hello From":
        _crypter, _score = "f4561bc239", 10.12
    elif text == "my":
        _crypter, _score = "3c", 35.07
    else:
        _crypter, _score = "129a99cd27", 2.19
    return _crypter, _score


text_blocks = ("Hello From", "oh noo, it's too big!!!!!", "my")


def sender(conn: Connection, text: str) -> None:
    text, score = crypter(text[:10])
    data = bytearray(text.encode()) + bytearray(b"\x20" * (10-len(text))) + struct.pack("d", score)
    conn.send_bytes(data)


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    _buffer = bytearray(b"\x00" * len(text_blocks)*18)
    pipes = [Pipe() for _ in range(len(text_blocks))]

    for text, connects in zip(text_blocks, pipes):
        Process(target=sender, args=(connects[0], text)).start()

    for i, connects in enumerate(pipes):
        connects[-1].recv_bytes_into(_buffer, i*18)

    for i, text in enumerate(text_blocks):
        cipher = _buffer[i*18:i*18+10].decode().strip()
        score = struct.unpack('d', _buffer[i*18+10:i*18+18])[0]
        print(f'text={text}; cipher={cipher}; score={score}')
