import multiprocessing
import time
from random import randint


class CSVHandler(multiprocessing.Process):
    def __init__(self, files: list[str] | tuple[str] = None, worker: callable = None, timeout: int = 1):
        # Напишите класс CSVHandler c атрибутами files, worker, timeout
        # который создает для кадого файла дочерний процесс обработки.
        # Если обработка затягивается, процесс "завис" и его нужно убить с очисткой ресурсов.
        # Для создания процессов используйте объект контекста
        super().__init__()
        self.files = files
        self.worker = worker
        self.timeout = timeout
        self.processes = []

    def run(self):
        ctx = multiprocessing.get_context()
        for file in self.files:
            pr = ctx.Process(target=self.worker, args=(file, ), daemon=True)
            pr.start()
            self.processes.append((file, pr))

        time.sleep(self.timeout)

        for file, pr in self.processes:
            if pr.is_alive():
                pr.terminate()
                pr.join()
                pr.close()
                print(f'{file} processing timeout exceeded')


def worker(file: str):
    i = randint(0, 4)
    time.sleep(i)
    print(file, i)


if __name__ == '__main__':
    filenames = ['file_1.csv', 'file_2.csv', 'file_3.csv']  # список файлов CSV для обработки
    csv_worker = CSVHandler(filenames, worker)
    csv_worker.timeout = 1
    csv_worker.start()
