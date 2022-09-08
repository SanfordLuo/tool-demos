"""
接口的压力测试demo
"""
import requests
import json
import threading
import uuid
from script import log_handler

logger = log_handler.Logger('pressure_by_threading.log').logger

# 用户token字典
# tokens = {'111': '111', '222': '222', '333': '333', '444': '444', '555': '555'}
url = 'http://okayapi-internal-test.xk12.cn/v1/ailearn/okminicourse-svc/v2/minicourse/share/k/page?teacher_id=62951736183&ktype=1&kid=672&org_id=640&share_state=1&page_index=1&page_size=10'
# kid=1828354&ktype=0&teacher_id=61951279137&org_id=80&share_state=0&page_index=1&page_size=10

def test_api(user_id, user_token):
    requestid = user_token + '-' + str(uuid.uuid4())
    headers = {
        'requestid': requestid
    }
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=5)
        resp = json.loads(response.text)
        logger.info(f'[{requestid}] 接口返回信息 user_id:{user_id}, resp:{resp}')
        if response.status_code == 200:
            logger.info(f'[{requestid}] 接口调用状态码为200 user_id:{user_id}')
        else:
            logger.error(f'[{requestid}] 状态码非200 user_id:{user_id}, status_code:{response.status_code}')
    except Exception as e:
        logger.error(f'[{requestid}] 调用接口失败 user_id:{user_id}, e:{e}')


def run():
    tokens = {str(i): str(i) for i in range(50)}
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
    # run()
    logger.error('fffffffffffffffff')
