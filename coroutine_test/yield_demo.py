"""
Python3.3
遇到 yield from 进行切换
1
3
4
2
"""


def func1():
    yield 1
    yield from func2()
    yield 2


def func2():
    yield 3
    yield 4


if __name__ == '__main__':
    f1 = func1()
    for item in f1:
        print(item)
