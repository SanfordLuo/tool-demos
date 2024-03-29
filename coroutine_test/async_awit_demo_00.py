"""
Python3.5
await 遇到 IO 耗时操作自动进行切换
1
3
4
2
"""
import asyncio


async def func1():
    print(1)
    await asyncio.sleep(2)
    print(2)


async def func2():
    print(3)
    await asyncio.sleep(1)
    print(4)


if __name__ == '__main__':
    tasks = [
        asyncio.ensure_future(func1()),
        asyncio.ensure_future(func2())
    ]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
