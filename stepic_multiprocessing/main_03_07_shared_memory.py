from multiprocessing import Process, shared_memory


def write_value(shm: shared_memory):
    buffer = shm.buf
    buffer[0] = 42
    print(f"Значение, записанное в память: {buffer[0]}")


def read_value(shm: shared_memory):
    buffer = shm.buf
    value = buffer[0]
    print(f"Прочитанное значение из памяти: {value}")


if __name__ == '__main__':
    shm = shared_memory.SharedMemory(create=True, size=1)

    # Создание процессов для записи и чтения значения из памяти
    process_write = Process(target=write_value, args=(shm,))
    process_read = Process(target=read_value, args=(shm,))

    # Запуск процессов и ожидание записи в память процесса write_value
    process_write.start()
    process_write.join()

    process_read.start()
    process_read.join()
