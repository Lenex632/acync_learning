def crypto_utils(text: str) -> str:
    if text.startswith("a"):
        return "aaa45678"
    if text.startswith("b"):
        return "bbb45678"

text_blocks =("allocation", "bombshell")


import multiprocessing
import ctypes


class Encrypter(multiprocessing.Process):
    def __init__(self, target: callable, args: str):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Array(ctypes.c_char, b" "*8)

    def run(self):
        res = self.target(self.args).encode()
        self.result.value = res


if __name__ == '__main__':
    results = {}

    processes = [Encrypter(target=crypto_utils, args=text) for text in text_blocks]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
        results[process.result.value.decode()] = process.args

    print(results)
