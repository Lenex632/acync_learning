import requests
import concurrent.futures

sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]


def get_request_header(url: str):
    return requests.get(url).headers


headers_stor = {}


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_request_header, url): url for url in sources}
        done, not_done = concurrent.futures.wait(futures, timeout=1.5)
        for f in done:
            headers_stor[futures[f]] = f.result()
        for f in not_done:
            headers_stor[futures[f]] = 'no_response'

    print(headers_stor)


if __name__ == '__main__':
    main()
