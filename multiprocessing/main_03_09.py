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
    def __init__(self, target: callable, text: str, shared_text: shared_memory.SharedMemory,
                 shared_num: shared_memory.SharedMemory, index: int):
        super().__init__()
        self.target = target
        self.text = text
        self.shared_text = shared_text.buf
        self.shared_num = shared_num.buf
        self.index = index * 8

    def run(self):
        text, num = self.target(self.text)
        self.shared_text[self.index:self.index + 8] = text.encode()
        self.shared_num[self.index:self.index + 8] = struct.pack('d', num)


if __name__ == '__main__':
    results = {}
    shared_text = shared_memory.SharedMemory(create=True, size=8 * len(text_blocks))
    shared_num = shared_memory.SharedMemory(create=True, size=8 * len(text_blocks))

    processes = []
    for index, text in enumerate(text_blocks):
        processes.append(Encrypter(target=crypto_utils, text=text, shared_text=shared_text, shared_num=shared_num, index=index))
    for process in processes:
        process.start()
    for i, process in enumerate(processes):
        process.join()
        i *= 8
        results[process.shared_text[i:i+8].tobytes().decode()] = (process.text, struct.unpack('d', process.shared_num[i:i+8])[0])

    print(results)
