import asyncio
import aiohttp
import datetime


async def request_test(session, url):
    print(f'{datetime.datetime.now()} 开始请求======{url}')
    async with session.get(url) as resp:
        print(resp.status)
        ret = await resp.text()
        # print(ret)

    print(f'{datetime.datetime.now()} 请求结束====={url}')


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            'https://api.github.com/events',
            'https://www.zhihu.com/',
            'http://www.baidu.com',
        ]
        # tasks = [asyncio.create_task(request_test(session, url)) for url in url_list]
        # asyncio.wait 源码内部会对列表中的每个协程执行ensure_future从而封装为Task对象
        tasks = [request_test(session, url) for url in url_list]

        # 过期时间内done为完成的，pending为未完成的
        done, pending = await asyncio.wait(tasks, timeout=3)
        # print(done, pending)

if __name__ == '__main__':
    asyncio.run(main())
