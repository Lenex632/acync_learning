import multiprocessing
import time


def task():
    print(multiprocessing.current_process().authkey)
    print("start")
    time.sleep(2)
    print("end")


def main():
    pr = multiprocessing.Process(target=task)
    pr.start()
    print("END")


if __name__ == '__main__':
    print(multiprocessing.current_process().authkey)
    main()
