import multiprocessing as mp


class MyProcess(mp.Process): # наследуем оригинальный класс Process

    def __init__(self, new_arg):  # переопределение инициализатора
        super().__init__()  # инициализация наследуемого класса mp.Process
        self.new_arg = new_arg  # создание дополнительных атрибутов при необходимости

    def run(self):  # переопределение метода run
        pass    # реализация целевой задачи процесса
