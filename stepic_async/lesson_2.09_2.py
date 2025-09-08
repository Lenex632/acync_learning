import socket
import selectors


def event_loop(server_socket: socket.socket) -> None:
    with selectors.DefaultSelector() as sel:
        sel.register(server_socket, selectors.EVENT_READ, accept_conn)
        while True:
            if not (events := sel.select(timeout=2)):
                print("Нет новых запросов за отведенный таймаут. Завершаем event_loop.")
                break
            for k, _ in events:
                sock: socket.socket = k.fileobj
                try:
                    k.data(sock, sel)
                except socket.error:
                    print("Потеря связи с клиентом. Закрываем сокет, снимаем с регистрации.")
                    sock.close()
                    sel.unregister(sock)
