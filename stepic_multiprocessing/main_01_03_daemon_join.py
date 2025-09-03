import multiprocessing
import time


def task():
    print("\tstart")
    print(f"\t{multiprocessing.current_process().name=}")
    time.sleep(2)
    print("\tend")


def main():
    print("START")
    pr = multiprocessing.Process(target=task, daemon=True)
    pr.start()
    pr.join(1)
    print(f"{multiprocessing.current_process().name=}")
    print(f"{pr.exitcode=}")  # выводит None, если в момент вызова процесс еще не завершился
    print("END")


if __name__ == '__main__':
    main()
