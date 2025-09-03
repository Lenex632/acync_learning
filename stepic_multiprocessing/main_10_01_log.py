import logging
from functools import wraps


config_log = {
    "level": logging.INFO,
    "filename": "files/log.txt",
    "filemode": "w",
    "format": "{processName}, {threadName}, {msg}, {asctime}",
    "style": "{"
}

logging.basicConfig(**config_log)


def loger(func: callable):
    def wrapper(*args, **kwargs):
        res = func()
        logging.info(func.__name__)
        return res
    return wrapper


@loger
def task():
    pass


if __name__ == '__main__':
    task()
