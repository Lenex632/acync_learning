from multiprocessing.connection import Listener
from array import array
from multiprocessing.connection import Client

address = ('localhost', 6000)  # используем TCP сокет

'''
Server
'''
# для создания объекта слушателя и соединения Connection удобно испльзовать менеджер with,
# который автоматически закроет соединение после использования
with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        # логируем факт успешного соединения и показываем использованный адрес
        print('connection accepted from', listener.last_accepted)

        # известными нам методами отправляем данные различных типов
        conn.send([2.25, None, 'junk', float])
        conn.send_bytes(b'hello')
        conn.send_bytes(array('i', [42, 1729]))

'''
Client
'''
# создаем соединение клиента и используем его как обычный Connection
with Client(address, authkey=b'secret password') as conn:
    # затем получаем данные в том порядке, в котором они были отосланы используя все известные
    # методы получения
    print(conn.recv())  # [2.25, None, 'junk', float]
    print(conn.recv_bytes())  # 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    # добавляем в существующий массив полученные данные, получаем 8 байт (2 знаения по 4 байта)
    print(conn.recv_bytes_into(arr))  # 8
    print(arr)  # array('i', [42, 1729, 0, 0, 0])