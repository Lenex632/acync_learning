import threading


class NoTargetException(Exception):
    def __init__(self, thread_name):
        super(NoTargetException, self).__init__()
        self.thread_name = thread_name


class MyThread(threading.Thread):
    def __init__(self, target=None, result=None):
        super(MyThread, self).__init__()
        self.target = target
        self.result = result

    def run(self) -> None:
        if not self.target:
            raise NoTargetException(self.name)
        else:
            self.result = self.target()


def custom_hook():
    print(f'{threading.current_thread().name} (id={threading.get_ident()}) failed')


if __name__ == '__main__':
    threading.excepthook = custom_hook
