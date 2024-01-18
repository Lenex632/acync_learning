import threading
import csv
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path


class Worker(threading.Thread):
    def __init__(self, target_dir: Path, out_dir: Path, threads_number: int = 2):
        super().__init__()
        self.target_dir = target_dir
        self.out_dir = out_dir
        self.threads = []
        self.sema = threading.Semaphore(threads_number)

    def add_normalized_price(self, file: Path) -> None:
        with self.sema:
            out_file = self.out_dir.joinpath(file.name)

            with open(file, 'r+', newline='') as file:
                reader = csv.reader(file)

                start_date = reader.__next__()
                start_num = start_date[1]
                date = [start_date + ['100']]

                for row in reader:
                    date.append(row + [str(float(row[1]) * 100 / float(start_num))])

            with open(out_file, 'w+', newline='') as file:
                writer = csv.writer(file)
                print(date)
                writer.writerows(date)

    def run(self):
        self.out_dir.mkdir(exist_ok=True)

        for file in self.target_dir.iterdir():
            self.threads.append(threading.Thread(target=self.add_normalized_price, name=f'{file.stem}_thread', args=(file, )))
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()


def main():
    target_dir = Path('files/out')
    out_dir = Path('files/out2')

    worker = Worker(target_dir, out_dir, 5)
    worker.start()
    worker.join()

    fig = go.Figure()
    for file in out_dir.iterdir():
        df = pd.read_csv(file)
        df.columns = ['date', 'prise', 'normal']
        fig.add_trace(go.Scatter(x=df['date'], y=df['normal'], name=file.stem))
    fig.show()


if __name__ == '__main__':
    main()
