import time
import json
import requests
from utils import const
from utils.util_encrypt import CipherHandler

device_id = const.API_DEVICE_IDS[0]


def test():
    timestamp = str(int(time.time() * 1000))
    data = {
        'content': [{
            'data': '点播歌曲'
        }],
        'userInfo': {
            'uniqueId': device_id
        }
    }

    # 参数加密, 需在机器人信息页面开启加密状态
    # http://biz.turingos.cn/robotMsg/5462
    cipher_handler = CipherHandler(timestamp)
    data = cipher_handler.encrypt(json.dumps(data))

    post_data = {
        'data': data,
        'key': const.API_KEY,
        'timestamp': timestamp
    }

    resp = requests.post(url=const.API_URL, data=json.dumps(post_data))
    return resp.text


if __name__ == '__main__':
    ret = test()
    print(ret)
