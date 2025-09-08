from inspect import getgeneratorstate


def echo_gen():
    value = None
    while True:
        try:
            value = yield value
        except StopIteration:
            return "StopIteration. Генератор завершил свою работу!"
        except Exception as e:
            value = yield f"Получено переданное исключение. Тип: {type(e).__name__}. Сообщение: {e}"


if __name__ == "__main__":
    g = echo_gen()

    print(g.send(None))
    print(g.send(1))
    print(g.throw(ValueError("oops!")))
    print(g.send(2))
    try:
        print(g.throw(StopIteration))
    except StopIteration as error:
        print(str(error))
    print(getgeneratorstate(g))

