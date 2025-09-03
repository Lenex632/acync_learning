import concurrent.futures
import time
import threading


def inition(*args):
    print(f"start initializer with {threading.current_thread().name} with {args=}")


def my_function(num):
    print(f"Start_processing_{num}_with_{threading.current_thread().name}")
    time.sleep(num)
    print(f"Finish_processing_{num}_with_{threading.current_thread().name}")
    return num * 2


def simple_example():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2, initializer=inition, initargs=(112, 911),
                                               thread_name_prefix="T") as executor:
        results = executor.map(my_function, [1, 2, 3, 4, 5])
        for result in results:
            print(result)


def some_exceptions():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(my_function, [1, 2, 3, 4, 3, 2, 1], timeout=11)
        while True:
            try:
                print(next(results))
            except concurrent.futures.TimeoutError:
                print("TimeoutError occurred")
            except StopIteration:
                print("StopIteration")
                break


def home_task():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        results = executor.map(my_function, [1, 2, 3, -4, 3, 2, 1])
        while True:
            try:
                print(next(results))
            except ValueError:
                print("External error from fn")
            except StopIteration:
                print("StopIteration")
                break


if __name__ == '__main__':
    # simple_example()
    # some_exceptions()
    home_task()
