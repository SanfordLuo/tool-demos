import asyncio


async def func_00():
    print('test')


if __name__ == '__main__':
    ret = func_00()

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(ret)

    # python3.7之后支持
    asyncio.run(ret)
