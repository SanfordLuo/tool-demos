import asyncio


async def func_00():
    aa = 1 / 0
    await asyncio.sleep(2)
    print("===== func_00")
    return "func_00"


async def func_01():
    await asyncio.sleep(1)
    print("===== func_01")
    return "func_01"


async def main():
    # return_exceptions=True: 将异常信息作为正常结果返回
    # return_exceptions=False: 抛出异常之后的任务不再处理
    ret = await asyncio.gather(*[func_00(), func_01()], return_exceptions=True)
    print(ret)


if __name__ == '__main__':
    run = main()
    asyncio.run(run)
