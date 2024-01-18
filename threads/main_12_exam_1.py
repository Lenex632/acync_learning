import concurrent.futures
import threading
import queue
import requests
import csv

from datetime import datetime, timezone
from pathlib import Path
from typing import Generator


# Константы
# Пути решил организовать с помощью библиотеки pathlib, по крайней мере для меня так удобнее
TARGET_DIR = Path('files/out')
TARGET_FILE = Path('files/tickers.txt')
START_DATE = '01.01.20'
END_DATA = '01.01.23'
MAIN_QUEUE = queue.Queue()


def get_history_data(ticker: str, start_date: str, end_date: str, interval: str = "1wk") -> (str, dict | None):
    """
    Получает исторические данные для указанного тикера актива.

    :param ticker: str, тикер актива.
    :param start_date: str, дата начала периода в формате 'дд.мм.гг'.
    :param end_date: str, дата окончания периода в формате 'дд.мм.гг'.
    :param interval: str, интервал времени (неделя, день и т.д.) (необязательный, по умолчанию '1wk' - одна неделя).
    :return: str, JSON-строка с историческими данными.
    """
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}'

    user_agent_key = "User-Agent"
    user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    headers = {user_agent_key: user_agent_value}

    per1 = int(datetime.strptime(start_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    per2 = int(datetime.strptime(end_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    params = {
        "period1": str(per1),
        "period2": str(per2),
        "interval": interval,
        "includeAdjustedClose": "true"
    }

    response = requests.get(url, headers=headers, params=params).json()
    return ticker, response


def get_ticker(file: Path) -> Generator[str, None, None]:
    """
    Генератор названий тикеров из файла.

    :param file: Path, путь к файлу с тикерами.
    :return:
    """
    with open(file) as file:
        for line in file:
            ticker = line.strip()
            yield ticker


def put_date_in_queue(future: concurrent.futures.Future):
    """
    Функция достаёт нужные данные из результата запроса и кладёт их в очередь для дальнейшей обработки.

    :param future: Future, футура с данными.
    :return: None.
    """
    name, data = future.result()
    # обработка, если обращение к API привело к ошибкам
    error = data['chart']['error']
    if error is not None:
        print(f'API error. Code: {error["code"]}, Description: {error["description"]}')
        return
    else:
        # Данные, по которым будем строить графики: начало недели - цена акции на конец недели
        # (это как я понял... я не силён в экономике и бирже... не бейте, пожалуйста)
        # TODO С временем у меня постоянные путаницы, особенно если надо в бд записывать.
        #  Не уверен корректно ли записывать его здесь в таком формате?
        time = list(map(lambda x: datetime.fromtimestamp(x).strftime('%d.%m.%Y'), data['chart']['result'][0]['timestamp']))
        price = data['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

        MAIN_QUEUE.put((name, time, price))


def write_to_file(target_dir: Path) -> None:
    """
    Функция берёт данные из очереди, создаёт файл с именем тикета и записывает туда данные.

    :param target_dir: Path, путь, в котором будут храниться все файлы.
    :return: None.
    """
    while True:
        name, time, price = MAIN_QUEUE.get()
        file = target_dir.joinpath(f'{name}.csv')
        date = [[time[i], price[i]] for i in range(len(time))]

        # запись в файл с помощью библиотеки csv
        with open(file, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(date)

        # помечаем задачу в очереди как завершённую
        MAIN_QUEUE.task_done()


def main():
    # запускаем пул потоков
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # запись осуществляем отдельным демоническим (ибо в функции бесконечный цикл) потоком
        # TODO не уверен должен ли он запускаться в пуле или отдельно?
        writer = threading.Thread(target=write_to_file, name='writer', args=(TARGET_DIR, ), daemon=True)
        writer.start()

        # создаём футуры для получения данных
        futures = [executor.submit(get_history_data, ticker, START_DATE, END_DATA) for ticker in get_ticker(TARGET_FILE)]
        for future in futures:
            exception = future.exception()
            # обработка, если реквест не пройдёт
            if exception is not None:
                print(f'An error occurred during downloading: {exception}')
            else:
                # если данные получены - запускаем обработчик с помощью колбэка
                future.add_done_callback(put_date_in_queue)

        # ждём завершения всех задач из очереди, после чего завершаем программу
        MAIN_QUEUE.join()


if __name__ == '__main__':
    main()
