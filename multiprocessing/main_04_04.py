def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


import multiprocessing as mp
from multiprocessing.managers import SyncManager


class Encrypter(mp.Process):
    def __init__(self, target: callable, data: str, sync_dict: SyncManager.dict):
        super().__init__()
        self.target = target
        self.data = data
        self.sync_dict = sync_dict

    def run(self):
        res, num = self.target(self.data)
        self.sync_dict[res] = (self.data, num)


if __name__ == '__main__':
    sync_dict = mp.Manager().dict()
    processes = []
    for text_block in text_blocks:
        process = Encrypter(target=crypto_utils, data=text_block, sync_dict=sync_dict)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print({k: v for k, v in sorted(sync_dict.items())})
