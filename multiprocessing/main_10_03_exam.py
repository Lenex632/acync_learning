import os
import requests
from PIL import Image
from time import perf_counter

import multiprocessing
import threading
import logging


logger = logging.getLogger('info_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="./nasa_foto/log.txt", mode="w")
handler.setFormatter(logging.Formatter(fmt="{asctime}, {msg}", style="{"))
logger.addHandler(handler)

error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(filename="./nasa_foto/error_log.txt", mode="w")
error_handler.setFormatter(logging.Formatter(fmt="{asctime}, {msg}", style="{"))
error_logger.addHandler(error_handler)


class Worker:
    def __init__(self, image_urls, output_directory, max_width, max_height, process_count):
        self.image_urls = image_urls
        self.output_directory = output_directory
        self.max_width = max_width
        self.max_height = max_height
        # Решил контролировать количество процессов через переменную
        self.process_count = process_count

        # Определяем папки
        self.original_dir = os.path.join(self.output_directory, "original")
        self.resized_dir = os.path.join(self.output_directory, "resized")

        # Создаём очередь
        self.queue = multiprocessing.JoinableQueue()

    def download(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            # Получаем имя файла из URL-адреса
            filename = url.split('/')[-1]
            # Сохраняем исходную картинку в папку "original"
            original_path = os.path.join(self.original_dir, filename)
            with open(original_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)
            logger.info(f'Успешно скачено изображение: {filename}')
            # Помещаем имя и путь до файла в очередь для изменения размера
            self.queue.put((filename, original_path))
        except requests.exceptions.RequestException as e:
            error_logger.error(f"Ошибка при обработке URL-адреса: {url}\nОшибка: {e}")

    def resize(self):
        while True:
            filename, original_path = self.queue.get()
            # Открываем исходную картинку с помощью PIL
            image = Image.open(original_path)
            # Масштабируем картинку до желаемых размеров
            image.thumbnail((max_width, max_height))
            # Создаем новое имя для уменьшенной копии
            resized_filename = f"resized_{filename}"
            # Сохраняем уменьшенную копию картинки в папке "resized"
            resized_path = os.path.join(self.resized_dir, resized_filename)
            image.save(resized_path)
            logger.info(f"Успешно создано уменьшенное изображение: {resized_filename}")
            # Помечаем задачу как завершённую, что бы определить время, когда следует останавливать всю работу
            self.queue.task_done()

    def start(self):
        os.makedirs(self.original_dir, exist_ok=True)
        os.makedirs(self.resized_dir, exist_ok=True)
        logger.info(f'Успешно созданы папки: {self.original_dir}, {self.resized_dir}')

        # Создаём конкурентные потоки для скачивания файлов
        ths = [threading.Thread(target=self.download, args=[url]) for url in urls]
        [th.start() for th in ths]

        # Создаём обрабатывающие процессы
        prs = [multiprocessing.Process(target=self.resize, daemon=True) for _ in range(self.process_count)]
        [pr.start() for pr in prs]

        # Ждём завершения скачивания файлов
        [th.join() for th in ths]
        # Ждём завершения обработки файлов
        self.queue.join()
        # Процессы демонические, но в каждом из них бесконечный цикл, так что завершаем их, на всякий случай
        for pr in prs:
            pr.terminate()
            pr.join()
            pr.close()


def download_and_resize_images(image_urls, output_directory, max_width, max_height):
    # Создаем папки для оригинальных картинок и уменьшенных версий
    original_dir = os.path.join(output_directory, "original")
    resized_dir = os.path.join(output_directory, "resized")
    os.makedirs(original_dir, exist_ok=True)
    os.makedirs(resized_dir, exist_ok=True)

    for url in image_urls:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Получаем имя файла из URL-адреса
            filename = url.split('/')[-1]

            # Сохраняем исходную картинку в папку "original"
            original_path = os.path.join(original_dir, filename)
            with open(original_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)

            # Открываем исходную картинку с помощью PIL
            image = Image.open(original_path)

            # Масштабируем картинку до желаемых размеров
            image.thumbnail((max_width, max_height))

            # Создаем новое имя для уменьшенной копии
            resized_filename = f"resized_{filename}"

            # Сохраняем уменьшенную копию картинки в папке "resized"
            resized_path = os.path.join(resized_dir, resized_filename)
            image.save(resized_path)
            print(f"Успешно создано уменьшенное изображение: {resized_filename}")

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при обработке URL-адреса: {url}")
            print(f"Ошибка: {e}")
        except IOError as e:
            print(f"Ошибка при обработке файла: {filename}")
            print(f"Ошибка: {e}")


urls = [
    'https://apod.nasa.gov/apod/image/2310/IC63_GruntzBax.jpg',
    'https://apod.nasa.gov/apod/image/2310/2P_Encke_2023_08_24JuneLake_California_USA_DEBartlett.jpg',
    'https://apod.nasa.gov/apod/image/2310/20231023_orionids_in_taurus_1440b.jpg',
    'https://apod.nasa.gov/apod/image/2310/Arp87_HubblePathak_2512.jpg',
    'https://apod.nasa.gov/apod/image/2310/C2023H2LemmonGalaxies.jpg',
    'https://apod.nasa.gov/apod/image/2310/WesternVeil_Wu_2974.jpg',
    'https://apod.nasa.gov/apod/image/2310/M33_Triangulum.jpg',
    'https://apod.nasa.gov/apod/image/2310/MuCephei_apod.jpg',
    'https://apod.nasa.gov/apod/image/2310/Hourglass_HubblePathak_1080.jpg',
    'https://apod.nasa.gov/apod/image/2310/HiResSprites_Escurat_3000.jpg',
    'https://apod.nasa.gov/apod/image/2309/M8-Mos-SL10-DCPrgb-st-154-cC-cr.jpg',
    'https://apod.nasa.gov/apod/image/2309/BlueHorse_Grelin_93.jpg',
    'https://apod.nasa.gov/apod/image/2309/Arp142_HubbleChakrabarti_2627.jpg',
    'https://apod.nasa.gov/apod/image/2309/HH211_webb_3846.jpg',
    'https://apod.nasa.gov/apod/image/2309/LRGBHa23_n7331r.jpg',
    'https://apod.nasa.gov/apod/image/2309/PolarRing_Askap_960.jpg',
    'https://apod.nasa.gov/apod/image/2309/STSCI-HST-abell370_1797x2000.jpg'
]
output_directory = "./nasa_foto"
max_width = 600
max_height = 400


if __name__ == '__main__':
    start_time = perf_counter()
    # download_and_resize_images(urls, output_directory, max_width, max_height)
    worker = Worker(urls, output_directory, max_width, max_height, 3)
    worker.start()
    logger.info(f"ALL DONE, {perf_counter() - start_time}")
    # Время на моей машине при последовательной работе: ~100-130с
    # Время на моей машине при параллельной работе: ~15-30с
