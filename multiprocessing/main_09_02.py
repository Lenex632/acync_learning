def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")


from concurrent.futures import ProcessPoolExecutor


if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        answers = executor.map(crypto_utils, text_blocks)

    results = {crypt: (text_block, num) for text_block, (crypt, num) in zip(text_blocks, answers)}
    print(results)
