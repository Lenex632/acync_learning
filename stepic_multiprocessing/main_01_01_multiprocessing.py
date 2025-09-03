import multiprocessing


def test():
    print("+")


def main():
    prs = [multiprocessing.Process(target=test) for _ in range(5)]
    for pr in prs:
        pr.start()


if __name__ == "__main__":
    multiprocessing.set_start_method('forkserver')

    main()
    print("+")

print("+")
