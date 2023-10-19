import concurrent.futures
import threading
import plotly

from pathlib import Path


TARGET_DIR = Path('files/out')


def add_normalized_price(file: Path) -> None:
    pass


def main():
    threads = []
    for file in TARGET_DIR.iterdir():
        threads.append(threading.Thread(target=add_normalized_price, name=f'{file.stem}_thread', args=(file, )))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
