import requests
from time import time


def get_file(url):
    r = requests.get(url, allow_redirects=True)
    return r


def write_file(response):
    # https://loremflickr.com/cache/resized/65535_52762952436_c3c6b46e79_320_240_nofilter.jpg
    filename = 'pictures/' + response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t = time()
    url = 'https://loremflickr.com/320/240'

    for i in range(10):
        write_file(get_file(url))

    print(time() - t)


if __name__ == '__main__':
    main()
