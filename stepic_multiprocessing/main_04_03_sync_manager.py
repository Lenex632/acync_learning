from multiprocessing.managers import SyncManager
import multiprocessing


def task(data):
    print(data.x)  # something
    print(data.y)  # {'1': 1, '2': 2}
    data.y = {'1': 1, '2': 3}


if __name__ == "__main__":
    sync_manager = multiprocessing.Manager()
    sync_manager: SyncManager  # аннотация для IDE
    namespase = sync_manager.Namespace()
    namespase.x = "something"
    namespase.y = {"1": 1, "2": 2}
    pr_1 = multiprocessing.Process(target=task, args=[namespase])
    pr_1.start()
    pr_1.join()
    print(namespase.y)  # {'1': 1, '2': 2}