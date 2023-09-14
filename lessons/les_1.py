"""
Основы сокетов, пример проблемы асинхронности.
Отдельно запустить сервер 'python3 lessons/les_1.py'.
Отдельно запустить клиентов 'nc localhost 5000'.
Два клиента не могут писать одновременно. Сначала пишет один, когда он "убивается" может начинать писать другой.
"""

import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 5000))
server_socket.listen()

while True:
    print('Before accept()')
    client_socket, addr = server_socket.accept()
    print('Connection from', addr)

    while True:
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hellow world\n'.encode()
            client_socket.send(response)

    print('Outside inner while loop')
    client_socket.close()
