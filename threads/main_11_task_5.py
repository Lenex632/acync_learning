import concurrent.futures
import time


def get_card_number():
    for i in range(801):
        yield str(4007000000100 + i)


def do_request(card_number: str):
    time.sleep(0.5)
    print(card_number)


def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        for card_number in get_card_number():
            executor.submit(do_request, card_number)


if __name__ == '__main__':
    main()
