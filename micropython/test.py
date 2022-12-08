class a():
    def __init__(self):
        self._a = 'this'
    def do(self):
        print(f'from a: {self._a}')
    def set(self, that):
        self._a = that


class b():
    def __init__(self, a):
        self.item = a

    def print_item(self):
        print('from b', self.item.do())

class c():
    def __init__(self, a):
        self.item = a

    def print_item(self):
        print('from c: ', self.item.do())


def main():
    A = a()
    B = b(A)
    C = c(A)

    #A.do()

    B.print_item()
    C.print_item()

    A.set('fdsa')

    B.print_item()
    C.print_item()

if __name__ == "__main__":
    main()