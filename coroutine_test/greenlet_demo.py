"""
pip install greenlet
遇到 switch 进行切换
1
lyf
3
2
4
"""
from greenlet import greenlet


def func1():
    print(1)
    gr2.switch('lyf')
    print(2)
    gr2.switch()


def func2(name):
    print(name)
    print(3)
    gr1.switch()
    print(4)


if __name__ == '__main__':
    gr1 = greenlet(func1)
    gr2 = greenlet(func2)
    gr1.switch()
