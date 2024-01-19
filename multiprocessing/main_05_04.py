def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


import multiprocessing as mp


class Encrypter(mp.Process):
    def __init__(self, target: callable, data: str, queue: mp.Queue):
        super().__init__()
        self.target = target
        self.data = data
        self.queue = queue

    def run(self):
        res, num = self.target(self.data)
        self.queue.put((res, (self.data, num)))


if __name__ == '__main__':
    queue = mp.Queue()
    processes = []
    for text_block in text_blocks:
        process = Encrypter(target=crypto_utils, data=text_block, queue=queue)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

    results = {}
    while not queue.empty():
        res, data = queue.get()
        results[res] = data
    print(results)
