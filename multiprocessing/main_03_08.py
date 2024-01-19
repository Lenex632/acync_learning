def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


from multiprocessing import Process, shared_memory
import struct


class Encrypter(Process):
    def __init__(self, target: callable, text: str, shared_text: shared_memory.SharedMemory, shared_num: shared_memory.SharedMemory):
        super().__init__()
        self.target = target
        self.text = text
        self.shared_text = shared_text.buf
        self.shared_num = shared_num.buf

    def run(self):
        text, num = self.target(self.text)
        self.shared_text[:len(text)] = text.encode()
        self.shared_num[:] = struct.pack('d', num)


if __name__ == '__main__':
    results = {}
    shared_text = shared_memory.SharedMemory(create=True, size=1024)
    shared_num = shared_memory.SharedMemory(create=True, size=8)

    processes = [Encrypter(target=crypto_utils, text=text, shared_text=shared_text, shared_num=shared_num) for text in text_blocks]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    for process in processes:
        results[process.shared_text[:8].tobytes().decode()] = (process.text, struct.unpack('d', process.shared_num[:])[0])

    print(results)
