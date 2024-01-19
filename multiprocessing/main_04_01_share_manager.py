from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp


def task(i, data, sml):
    sml[i] = sum(data)


if __name__ == "__main__":
    # Создаем экземпляр менеджера
    shm_mng = SharedMemoryManager()
    # Запускаем. Создается дочерний процесс диспетчер
    shm_mng.start()
    print(f"{mp.active_children()=}")  # информация о процессе диспетчере

    shm_list = shm_mng.ShareableList(range(10))  # создаем объект список с общей памятью
    print(shm_list)  #
    shm_list[0] = 100  # работаем с ним как привыкли используя индексацию или срезы
    print(shm_list)  #
    shm_sm = shm_mng.SharedMemory(10)  # создаем объект общей памяти
    print(shm_sm)  #
    shm_sm.buf[0:2] = b"ab"  # работаем с ним как с массивом байт
    shm_sm.buf[2:4] = b"12"
    print(*shm_sm.buf[:])

    shm_mng.shutdown()  # очищаем ресурсы (вызываются методы unlink для всех использующих shm_mng процессов)

    print('-'*100)
    with SharedMemoryManager() as shm_mng:
        sml = shm_mng.ShareableList(range(2))
        pr_1 = mp.Process(target=task, args=(0, (10, 20, 30), sml))
        pr_2 = mp.Process(target=task, args=(1, (40, 50, 60), sml))
        pr_1.start()
        pr_2.start()
        pr_1.join()
        pr_2.join()
        print(sml[0], sml[1])  # 60, 150