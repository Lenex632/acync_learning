def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


from multiprocessing import Process, shared_memory


class Encrypter(Process):
    def __init__(self, target: callable, text: str, shared_list: shared_memory.ShareableList, index: int):
        super().__init__()
        self.target = target
        self.text = text
        self.shared_list = shared_list
        self.index = index * 2

    def run(self):
        text, num = self.target(self.text)
        self.shared_list[0 + self.index] = num
        self.shared_list[1 + self.index] = text
        self.shared_list.shm.close()


if __name__ == '__main__':
    results = {}
    data = [3.14, 'a' * 8] * len(text_blocks)
    shared_list = shared_memory.ShareableList(data)

    processes = []
    for index, text in enumerate(text_blocks):
        processes.append(Encrypter(target=crypto_utils, text=text, shared_list=shared_list, index=index))
    for process in processes:
        process.start()
    for i, process in enumerate(processes):
        process.join()
        i *= 2
        results[process.shared_list[1 + i]] = (process.text, process.shared_list[0 + i])

    shared_list.shm.close()
    shared_list.shm.unlink()
    print(results)
