import concurrent.futures
import time

# Напишите функцию post_worker
# Создайте пул потоков и запустите выполнение целевой задачи worker, после получения результатов
# запустите функцию пост обработчика результата. Если при получении результата возбуждаются исключения, выведите
# сообщение в консоль.


def worker(x):
    time.sleep(0.1 * x)
    return x


def post_worker(future):
    print(f'{future.result()} saved')


def main():
    sources = [1, 2, None, 4, 5]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(worker, i) for i in sources]
        for future in futures:
            exception = future.exception()
            #  лучше сначала обрабатывать ошибки, а колбеком вызывать только "удачные футуры"
            if exception is not None:
                print(exception)
            else:
                future.add_done_callback(post_worker)


if __name__ == '__main__':
    main()
