from time import perf_counter, sleep
import concurrent.futures


def worker(i):
    sleep(i)
    return i


def submit_vs_map():
    arr = [5, 4, 3, 2, 1]

    start = perf_counter()
    print("Используем метод submit() для создания будущих объектов")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(worker, i) for i in arr]
        # Получаем результаты задач в порядке их завершения и не ждем завершения всех сразу
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(result)
    print(f"Итого, выполнение за {perf_counter() - start:.4f}")

    start = perf_counter()
    print("Используем метод map() для выполнения задач в том же порядке что и располож. элем. в arr")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(worker, arr))
        # Выводим результаты выполнения задач в порядке, соответствующем порядку элементов в итерируемом объекте
        for result in results:
            print(result)
    print(f"Итого, выполнение за {perf_counter() - start:.4f}")


def my_function(num):
    sleep(num)
    return num * 2


def who_s_faster():
    start_time = perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results_map = list(executor.map(my_function, [1, 2, 3, 4]))
        print(perf_counter() - start_time)  # печатаем время выполнения с использованием map
        print(*results_map)

    start_time = perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        results_submit = [executor.submit(my_function, arg) for arg in [1, 2, 3, 4]]
        print(perf_counter() - start_time)  # печатаем время выполнения с использованием submit
        print(*results_submit)


def main_result_magic():
    sources = ["A",
               "B",
               "C",
               "D",
               "E"]

    def test(source: str):
        if source == "A":
            sleep(1.2)
        if source == "B":
            sleep(1.9)
        if source == "C":
            sleep(0.5)
        if source == "D":
            sleep(2)
        if source == "E":
            sleep(3.5)
        return source

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(test, source): source for source in sources}
        for future, source in futures.items():
            try:
                print(future.result(1.5), source)
            except concurrent.futures._base.TimeoutError:
                print("TimeoutError", source)


def issue(x):
    return 4 // x


def map_issue():
    arr = [1, 2, 0, 4, 5]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(issue, arr))
        for result in results:
            print(result)


def submit_issue():
    arr = [1, 2, 0, 4, 5]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(issue, i) for i in arr]
        for future in futures:
            try:
                print(future.result())
            except ZeroDivisionError:
                print('Error')


if __name__ == '__main__':
    # submit_vs_map()
    # who_s_faster()
    # main_result_magic()
    # map_issue()
    submit_issue()
