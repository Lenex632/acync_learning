import socket
import select
from typing import Callable, List


def idle_select(sockets: List[socket.socket], idle_handler: Callable, timeout: int | float) -> List[socket.socket]:
    sockets_for_read, _, _ = select.select(sockets, [], [], timeout)
    if not sockets_for_read:
        idle_handler()
        return []
    else:
        return sockets_for_read

