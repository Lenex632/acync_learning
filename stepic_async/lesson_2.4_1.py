def my_awesome_gen():
    message = yield "Hello!"
    while True:
        if message.isalpha():
            message = yield message.capitalize()
        else:
            message = yield message.lower()


if __name__ == "__main__":
    g = my_awesome_gen()
    assert g.send(None) == "Hello!"
    assert g.send("COOL!") == "cool!"
    assert g.send("Das Auto") == "das auto"
    assert g.send("nIcE") == "Nice"
