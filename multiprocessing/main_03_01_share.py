import multiprocessing
import ctypes


class MyProcess(multiprocessing.Process):
    def __init__(self, target, args=()):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Array("u", " "*30)  # ctypes.c_wchar

    def run(self):
        result = self.target(*self.args)
        for i, s in enumerate(result):
            self.result[i] = s


def test(a: int, b: int):
    return f"{a} Х {b} = {a*b}"


def main():
    processes = [MyProcess(target=test, args=(i, i+1)) for i in (1, 2, 3)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    result = "\n".join(process.result[:].strip() for process in processes)
    print(result)


if __name__ == "__main__":
    main()
