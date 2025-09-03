import multiprocessing
import ctypes


class MyProcess(multiprocessing.Process):
    def __init__(self, target, args=()):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Value("i", 0)  # ctypes.c_int

    def run(self):
        result = self.target(*self.args)
        self.result.value = result


def test(a: int, b: int):
    return a*b


def main():
    processes = [MyProcess(target=test, args=(i, i+1)) for i in (1, 2, 3)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    result = "\n".join(f"{' X '.join(map(str, process.args))} = {process.result.value}" for process in processes)
    print(result)


if __name__ == "__main__":
    main()
