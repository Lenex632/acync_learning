from time import sleep, perf_counter
import threading

res = 0
start_time = perf_counter()  # запускаем отсчет времени проверки решения
card = 4007000000028


def do_request(card_number: str):
    global res
    sleep(2)
    res += 1
    print(f'{res} - {card_number} \n')


def init_thr():
    for i in range(71):
        do_request(str(card + i))


if __name__ == '__main__':
    tasks = [threading.Thread(target=do_request, args=(str(card + i), ), daemon=True).start() for i in range(71)]
    sleep(4)
    print(perf_counter() - start_time)

    assert perf_counter() - start_time <= 5
