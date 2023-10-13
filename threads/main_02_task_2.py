from time import sleep, perf_counter
import threading

headers_stor = {}
sources = ["bing.com",
           "google.ru",
           "yahoo.com",
           "mail.ru",
           "ya.ru"]
start_time = perf_counter()  # запускаем отсчет времени проверки решения


def get_request_header(url: str):
    if url == "yahoo.com":
        sleep(10)
    elif url == "mail.ru":
        sleep(1.8)
    elif url == "google.ru":
        sleep(0.2)
    else:
        sleep(1.4)
    headers_stor[url] = "ok"


def main_thread():
    tasks = [threading.Thread(target=get_request_header, args=(source, ), daemon=True) for source in sources]
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()


if __name__ == '__main__':
    main_thr = threading.Thread(target=main_thread, daemon=True)
    main_thr.start()
    main_thr.join(1.5)

    for source in sources:
        headers_stor.setdefault(source, "no_response")

    '''
    for url in sources:
        threading.Thread(target=get_request_header, args=[url], daemon=True).start()
    sleep(1.5)
    for url in sources:
        headers_stor.setdefault(url, "no_response")
    '''

    assert perf_counter() - start_time <= 2  # проверка того, что решение выполняется не более 2 секунд

    print(", ".join(f'{k}-{v}' for k, v in sorted(headers_stor.items())))


