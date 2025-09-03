import multiprocessing
import ctypes


class MyProcess(multiprocessing.Process):
    def __init__(self, target=None, args=None):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Value("d", 0)

    def run(self):
        result = self.target(*self.args)
        self.result.value = result


class MinMaxAvr(multiprocessing.Process):
    def __init__(self, target, args=()):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Array(ctypes.c_int, 3)

    def run(self):
        nums = self.target(*self.args)
        for i, num in enumerate(nums):
            self.result[i] = num
