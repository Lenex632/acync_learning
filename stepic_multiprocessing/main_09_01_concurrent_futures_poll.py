from concurrent.futures import ProcessPoolExecutor
import time
import multiprocessing


def inition(*args):
    print(f"start initializer with {multiprocessing.current_process().name} with {args=}")


def my_function(num):
    print(f"Start_processing_{num}_with_{multiprocessing.current_process().name}")
    time.sleep(num)
    print(f"Finish_processing_{num}_with_{multiprocessing.current_process().name}")
    return num * 2


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2,
                             initializer=inition, initargs=(112, 911),
                             max_tasks_per_child=None) as executor:
        results = executor.map(my_function, [2, 3, 4, 0, 1, 5])
        for result in results:
            print(result)
