def g_average():
    count = 1
    summa = 0
    average = None
    while True:
        try:
            average = yield average
            summa += average
            average = summa / count
            count += 1
        except Exception as e:
            return average, e.__class__.__name__, str(e)


if __name__ == "__main__":
    g = g_average()

    print(g.send(None))  # выводит None
    print(g.send(0))  # выводит 0.0
    print(g.send(10))  # выводит 5.0, т.к. (0 + 10) / 2
    print(g.send(20))  # выводит 10.0, т.к. (0 + 10 + 20) / 3
    print(g.send(0))  # выводит 7.5

    try:
        g.throw(ValueError("new_throw_msg"))
    except StopIteration as err:  # здесь обрабатываем завершение генератора
        avr, err, msg = err.value
        print(avr, err, msg)  # выводит три значения через пробел: 7.5 ValueError new_throw_msg

