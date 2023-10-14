import time

import requests
from requests.structures import CaseInsensitiveDict
import threading


class GetHeaders(threading.Thread):
    global result

    def __init__(self, url: str):
        super(GetHeaders, self).__init__()
        self.url = url
        self.url_headers = {}

    def run(self) -> None:
        self.url_headers[self.url] = get_request_header(self.url)


sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]


def get_request_header(url: str) -> CaseInsensitiveDict[str]:
    return requests.get(url).headers


if __name__ == '__main__':
    result = {}
    tasks = [GetHeaders(url) for url in sources]

    for task in tasks:
        task.start()
    for task in tasks:
        task.join(2)
        result.update(task.url_headers)
