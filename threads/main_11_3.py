import concurrent.futures
import requests


def download(url):
    response = requests.get(url)
    return response.content


def print_result(future):
    content = future.result()
    print(content)


def main_single():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(download, 'https://example.com')
        future.add_done_callback(print_result)


def main_multi():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download, 'https://example.com') for _ in range(5)]
    for future in futures:
        future.add_done_callback(print_result)


if __name__ == '__main__':
    # main_single()
    main_multi()
