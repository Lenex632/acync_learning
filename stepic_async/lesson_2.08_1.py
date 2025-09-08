import socket
import selectors
from typing import Callable, List


def idle_selectors(sockets: List[socket.socket], idle_handler: Callable, timeout: int | float) -> List[socket.socket]:
    with selectors.DefaultSelector() as sel:
        for sock in sockets:
            sel.register(sock, selectors.EVENT_READ)
        sockets_for_read = sel.select(timeout=timeout)
        if not sockets_for_read:
            idle_handler()
            return []
        else:
            return [s.fileobj for s, _ in sockets_for_read]

