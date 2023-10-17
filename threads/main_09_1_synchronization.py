import threading

n = 0


def task_increment():
    global n
    while n <= 1000:
        with open("files/f_in.txt", "a") as file:
            n += 1
            tmp = str(n) + "\n"
            file.write(tmp)


def task_write():
    while n <= 1000:
        with open("files/f_in.txt", "r") as f_read:
            try:
                x = f_read.read().split()[-1]
                if x:
                    x = int(x)
            except IndexError as err:
                print(err)
        if x % 2 == 0:
            with open("files/f_in.txt", "r") as f_read, open("files/f_out.txt", "a") as f_out:
                f_out.write(f"{f_read.read().split()[-1]}\n")


if __name__ == '__main__':
    th_1 = threading.Thread(target=task_increment)
    th_2 = threading.Thread(target=task_write)
    th_2.start()
    th_1.start()
    th_1.join()
    th_2.join()
