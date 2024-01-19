def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager


class Encrypter(Process):
    def __init__(self, target: callable, data: str, shared_list: SharedMemoryManager.ShareableList, index: int):
        super().__init__()
        self.target = target
        self.data = data
        self.shared_list = shared_list
        self.index = index * 2

    def run(self):
        text, num = self.target(self.data)
        self.shared_list[0 + self.index] = num
        self.shared_list[1 + self.index] = text


if __name__ == '__main__':
    results = {}
    with SharedMemoryManager() as shm_mng:
        shared_list = shm_mng.ShareableList([0, ' ' * 8] * len(text_blocks))
        processes = []
        for index, text_block in enumerate(text_blocks):
            process = Encrypter(target=crypto_utils, data=text_block, shared_list=shared_list, index=index)
            processes.append(process)
            process.start()
        for i, process in enumerate(processes):
            process.join()
            i *= 2
            results[process.shared_list[1 + i]] = (process.data, process.shared_list[0 + i])

    print(results)
