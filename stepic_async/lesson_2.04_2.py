def my_awesome_gen():
    dummy = 0
    while True:
        value = yield dummy
        if type(value) is int:
            dummy += value
        elif type(value) is float:
            dummy *= value
        else:
            return "Ошибка: введите число типа int или float"


if __name__ == "__main__":
    g = my_awesome_gen()

    assert g.send(None) == 0
    assert g.send(10) == 10
    assert g.send(11) == 21
    assert g.send(0.5) == 10.5
    assert g.send(100) == 110.5

    try:
        assert g.send("ok") is None
    except StopIteration as e:
        assert e.value == "Ошибка: введите число типа int или float"

