import requests
import concurrent.futures


sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]


def get_request_header(url: str):
    return requests.get(url).headers


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(sources)) as executor:
        results = list(executor.map(get_request_header, sources))

    headers_stor = dict(zip(sources, results))
    for item in headers_stor.items():
        print(item)


if __name__ == '__main__':
    main()
