"""
接口的压力测试demo
"""
import requests
import json
import threading
from script import log_handler

logger = log_handler.Logger('pressure_by_threading.log').logger

# 用户token字典
tokens = {'111': '111', '222': '222', '333': '333', '444': '444'}
url = 'https://event.csdn.net/logstores/csdn-pc-tracking-page-exposure/track'


def test_api(user_id, user_token):
    headers = {
        'Authorization': 'Bearer {0}'.format(user_token)
    }
    try:
        response = requests.post(
            url=url,
            headers=headers,
            timeout=5)
        resp = json.loads(response.text)
        logger.info('接口返回信息 user_id:{0}, resp:{1}'.format(user_id, resp))
        if response.status_code == 200:
            logger.info(u'接口调用状态码为200 user_id:{0}'.format(user_id))
        else:
            logger.error(u'状态码非200 user_id:{0}, status_code:{1}'.format(user_id, response.status_code))
    except Exception as e:
        logger.error(u'调用接口失败 user_id:{0}, e:{1}'.format(user_id, e))


def run():
    threads_list = []
    # 创建线程
    for k, v in tokens.items():
        t = threading.Thread(target=test_api, args=(k, v))
        threads_list.append(t)

    # 开启线程
    for i in threads_list:
        i.start()
    for i in threads_list:
        i.join()


if __name__ == '__main__':
    run()
