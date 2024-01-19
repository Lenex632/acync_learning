import multiprocessing
from multiprocessing import sharedctypes
import ctypes
from time import sleep


class ValueExample:
    def __init__(self, shared_value):
        self.shared_value = shared_value

    def change(self):
        with self.shared_value.get_lock():  # защищаем изменение значения блокировкой
            sleep(0.01)
            self.shared_value.value += 1
            sleep(0.01)
            self.shared_value.value -= 1


class RawValueExample:
    def __init__(self, raw_shared_value):
        self.shared_value = raw_shared_value

    def change(self):
        sleep(0.01)
        self.shared_value.value += 1
        sleep(0.01)
        self.shared_value.value -= 1


def worker_val(shared_value):
    value_example = ValueExample(shared_value)
    for _ in range(100):
        value_example.change()


def worker_rval(shared_value):
    raw_value_example = RawValueExample(shared_value)
    for _ in range(100):
        raw_value_example.change()


if __name__ == '__main__':
    # Создание экземпляра Value
    shared_value1 = multiprocessing.Value(ctypes.c_int, 0)

    # Создание экземпляра RawValue
    shared_value2 = sharedctypes.RawValue(ctypes.c_int, 0)

    # Создание двух процессов
    process_1 = multiprocessing.Process(target=worker_val, args=(shared_value1,))
    process_2 = multiprocessing.Process(target=worker_val, args=(shared_value1,))
    process_r_1 = multiprocessing.Process(target=worker_rval, args=(shared_value2,))
    process_r_2 = multiprocessing.Process(target=worker_rval, args=(shared_value2,))

    # Запуск процессов
    process_1.start()
    process_2.start()
    process_r_1.start()
    process_r_2.start()

    # Ожидание завершения процессов
    process_1.join()
    process_2.join()
    process_r_1.join()
    process_r_2.join()

    # Вывод результатов
    print("Value: ", shared_value1.value)
    print("RawValue: ", shared_value2.value)