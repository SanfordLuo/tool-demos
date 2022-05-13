"""
Python3.4
yield from 遇到 IO 耗时操作自动进行切换
1
3
4
2
"""
import asyncio


@asyncio.coroutine
def func1():
    print(1)
    yield from asyncio.sleep(2)
    print(2)


@asyncio.coroutine
def func2():
    print(3)
    yield from asyncio.sleep(1)
    print(4)


if __name__ == '__main__':
    tasks = [
        asyncio.ensure_future(func1()),
        asyncio.ensure_future(func2())
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
