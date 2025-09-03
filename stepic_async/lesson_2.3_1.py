from typing import Generator


def task_1():
    for i in range(1, 5):
        yield i


def task_2():
    for s in "AB":
        yield s


g1 = task_1()
g2 = task_2()


def task_manager(tasks: tuple[Generator] | list[Generator]) -> None:
    queue = [task for task in tasks]
    while queue:
        task = queue.pop(0)
        try:
            print(next(task))
        except StopIteration:
            print(f'Задача {task.__name__} завершена!')
        else:
            queue.append(task)


if __name__ == "__main__":
    task_manager((g1, g2))

