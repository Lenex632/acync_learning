from multiprocessing import shared_memory
for data in ([], [None, ], [0, ], [1, ], [5, ], [5, 6], "Лабрадор",
             [3.14159, 999_999_999, "awesome!"], ("a", "abcd"), ["Привет!", "Hellow!"]):
    sml = shared_memory.ShareableList(data)
    print("-"*100)
    for value in sml:
        print(value)
    print(sml.format)  # из интереса смотрим на структуру
    print(*sml.shm.buf[:])  # из интереса смотрим на массив байт
    sml.shm.close()
    sml.shm.unlink()
