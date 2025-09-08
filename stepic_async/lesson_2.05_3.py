from inspect import getgeneratorstate


def pow_gen():
    value = 0
    while True:
        try:
            value = yield value**2 if type(value) is int else 0
        except GeneratorExit:
            print("Generator pow_gen was closed!")
            return


if __name__ == "__main__":
    # сначала проверим завершение используя close в пользовательском коде
    g = pow_gen()
    next(g)
    print(g.send(2))
    print(g.send("A"))
    print(g.send(1))
    g.close()  # должно быть выведено сообщение согласно заданию
    print(getgeneratorstate(g))  # генератор должен быть закрыт

    # затем проверим, что сообщение о завершении будет выведено и при вызове close сборщиком мусора
    g = pow_gen()
    next(g)
    print(g.send("B"))
    print(g.send(3))
