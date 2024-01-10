import multiprocessing
import time


def task():
    print("\tstart")
    print(f"\t{multiprocessing.current_process().name=}")
    pr = multiprocessing.Process(target=task_2)
    pr.start()
    time.sleep(2)
    print("\tend")


def task_2():
    print(f"\t\t{multiprocessing.current_process().name=}")


def main():
    print("START")
    pr = multiprocessing.Process(target=task)  # daemon = only False
    pr.start()
    print("END")


if __name__ == '__main__':
    main()
