import concurrent.futures
import requests
import os
import queue
import threading

urls = [
    'https://apod.nasa.gov/apod/image/2306/NGC-6872-LRGB-rev-5-crop-CDK-1000-22-May-2023.jpg',
    'https://apod.nasa.gov/apod/image/2306/corona_aus.jpg',
    'https://apod.nasa.gov/apod/image/2306/LagoonCenter_HubblePobes_3979.jpg',
    'https://apod.nasa.gov/apod/image/2306/M15-3.jpg',
    'https://apod.nasa.gov/apod/image/2306/Shark_Kennedy_4176.jpg',
    'https://apod.nasa.gov/apod/image/2306/IssMoon_Yang_2599.jpg'
]


def download_file(url: str, timeout=1):
    """Функция для скачивания файла по указанному URL-адресу."""
    try:
        r = requests.get(url, stream=True, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        raise ValueError(f'Timeout error occurred during downloading file from url {url}')
    except Exception:
        raise ValueError(f'Unknown error occurred during downloading file from url {url}')
    else:
        if r.status_code == 200:
            return r.content, url
        else:
            raise ValueError(f'Failed to download file from url {url}')


def save_file_with_queue(data, filename):
    """Функция для сохранения файла в указанной директории с использованием очереди."""
    file_queue.put((data, filename))


def handle_task_done(future):
    """Функция-обработчик на завершение задачи."""
    exception = future.exception()
    if exception is not None:
        print(f'An error occurred during downloading: {exception}')
    else:
        result, url = future.result()
        save_file_with_queue(result, os.path.basename(url))


def file_writer():
    """Функция-поток для записи файлов из очереди на диск."""
    while True:
        data, filename = file_queue.get()
        os.makedirs('nasa_pic', exist_ok=True)
        with open(os.path.join('nasa_pic', filename), 'wb') as f:
            f.write(data)
        print(f'{filename} was saved successfully')
        file_queue.task_done()


def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for url in urls:
            future = executor.submit(download_file, url)
            future.add_done_callback(handle_task_done)

    # Ожидаем завершения всех задач в очереди перед выходом из программы
    file_queue.join()


if __name__ == '__main__':
    # Создаем очередь для сохранения файлов
    file_queue = queue.Queue()

    # Создаем поток для записи файлов на диск
    t = threading.Thread(target=file_writer)
    t.daemon = True
    t.start()

    main()
