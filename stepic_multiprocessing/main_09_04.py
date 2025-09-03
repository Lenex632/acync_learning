def get_image(url: str):
    print(url)
    url += ' file'
    return url


def image_processing(file: str):
    print(file)
    file += ' new'
    return file


def save_image(file: str):
    print(file)
    pass


import concurrent.futures


def one_image_processing(url):
    file = get_image(url)
    new_file = image_processing(file)
    return new_file


def save_to_server(future):
    file = future.result()
    save_image(file)


def group_image_processing(file_source: str) -> None:
    urls = []
    file = open(file_source, 'r+')
    for line in file:
        urls.append(line.strip())

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(one_image_processing, url) for url in urls]
        for future in futures:
            future.add_done_callback(save_to_server)


if __name__ == '__main__':
    file_source = 'files/urls.txt'
    group_image_processing(file_source)
