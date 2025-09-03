import time


def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("boom"):
        raise ValueError("timeout")
    if text.startswith("b"):
        time.sleep(2)
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "boom", "doom")


import concurrent.futures


results = {}
errors = {}


def crypto_handler(timeout: float | int = 2) -> None:
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     processes = [executor.submit(crypto_utils, text) for text in text_blocks]
    #     time.sleep(timeout)
    #     for i, text in enumerate(text_blocks):
    #         if processes[i].done():
    #             try:
    #                 crypt, num = processes[i].result()
    #                 results[crypt] = (text, num)
    #             except Exception as e:
    #                 errors[text] = e
    #         else:
    #             errors[text] = 'timeout_error'

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = {executor.submit(crypto_utils, text): text for text in text_blocks}
        done, not_done = concurrent.futures.wait(processes, timeout)
        for future in done:
            text = processes[future]
            if future.exception() is None:
                cipher, score = future.result()
                results[cipher] = (text, score)
            else:
                errors[text] = future.exception()
        for future in not_done:
            text = processes[future]
            errors[text] = "timeout_error"


if __name__ == "__main__":
    crypto_handler(1)
    print(results)
    print(errors)
