def g_task():
    text = f"{(yield ';)')} + {(yield 200)**(yield - 2 + 10)} = {(yield)}"
    print(text)


g = g_task()
print(g.send(10))
print(g.send(4))
