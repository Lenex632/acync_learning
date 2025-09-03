from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

# создается новый класс Точка, для этого наследуется Structure
class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]


def modify(n, x, s, A):
    n.value **= 2  # меняем значение int объекта Value
    x.value **= 2  # меняем значение float объекта Value
    s.value = s.value.upper()  # меняем строковое значение Array
    #  а здесь меняем атрибуты класса Point, обращаясь к точкам как к элементам массива Array
    for a in A:
        a.x **= 2
        a.y **= 2


if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)  # создаем значение по умолчанию 7, блокировка - по умолчанию
    x = Value(c_double, 1.0 / 3.0, lock=False)  # здесь значение с плав. точкой двойной точности
    s = Array('c', b'hello world', lock=lock)  # байтовая строка, блокировка - объект Lock
    # Здесь заполняем массив создавая экземпляры точек
    A = Array(Point, [(1.875, -6.25), (-5.75, 2.0), (2.375, 9.5)], lock=lock)

    p = Process(target=modify, args=(n, x, s, A))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value)
    print([(a.x, a.y) for a in A])