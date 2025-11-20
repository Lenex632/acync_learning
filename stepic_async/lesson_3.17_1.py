from inspect import (
    iscoroutinefunction,
    isgeneratorfunction,
    isasyncgenfunction,
    iscoroutine,
    isgenerator,
    isasyncgen
)

functions = []
func_coro = []
func_gen = []
async_func_gen = []
ob_coro = []
ob_gen = []
ob_async_gen = []

entities = []

for e in entities:
    if isasyncgenfunction(e):
        async_func_gen.append(e)
    elif isasyncgen(e):
        ob_async_gen.append(e)
    elif iscoroutinefunction(e):
        func_coro.append(e)
    elif iscoroutine(e):
        ob_coro.append(e)
    elif isgeneratorfunction(e):
        func_gen.append(e)
    elif isgenerator(e):
        ob_gen.append(e)
    else:
        functions.append(e)

