import threading
from typing import Callable


class SimpleThread(threading.Thread):
    def __init__(self, function: Callable = None, data=None):
        super(SimpleThread, self).__init__()
        self.function = function
        self.data = data

    def run(self):
        print(self.function(self.data))
