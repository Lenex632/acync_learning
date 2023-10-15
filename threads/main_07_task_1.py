class CCD:
    def __init__(self, d):
        self.cat: str = d['cat']
        self.union: bool = d['union']
        self.cargo: dict = d['cargo']
        self.id: int = d['id']

    def __lt__(self, other):
        t1 = (self.union, self.cat.startswith('020'), -self.id)
        t2 = (other.union, other.cat.startswith('020'), -other.id)
        return t1 > t2


if __name__ == '__main__':
    cats = ['0' + str(i) for i in range(201, 210)]
    print(cats)
