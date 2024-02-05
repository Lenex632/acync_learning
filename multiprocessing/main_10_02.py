def get_image(url: str):
    print(url)
    if url == 'url 2':
        raise TypeError('msg_err')
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
import logging
import multiprocessing


logger = multiprocessing.get_logger()
logger.setLevel(logging.ERROR)
fh = logging.FileHandler("files/log_errors.txt")
fh.setFormatter(logging.Formatter(fmt="{processName}, {asctime}, {msg[0]}, {msg[1]}", style='{'))
logger.addHandler(fh)


def handler(url: str) -> str:
    try:
        file = get_image(url)
    except Exception as e:
        logger.error((get_image.__name__, e))

    try:
        result = image_processing(file)
    except Exception as e:
        logger.info((image_processing.__name__, e))

    return result


def callback_save(future: concurrent.futures.Future) -> None:
    new_file = future.result()
    try:
        save_image(new_file)
    except Exception as e:
        logger.info((save_image.__name__, e))


def group_image_processing(file_source: str) -> None:
    with open(file_source) as file:
        urls = file.read().split('\n')
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for url in urls:
            future = executor.submit(handler, url)
            future.add_done_callback(callback_save)


if __name__ == '__main__':
    file_source = 'files/urls.txt'
    group_image_processing(file_source)
