import time
import json
import requests
from utils import const
from utils.util_encrypt import CipherHandler

device_id = const.API_DEVICE_IDS[0]


def test():
    timestamp = str(int(time.time() * 1000))
    data = {
        'perception': {'audition': {'text': '周杰伦'}},
        'reqType': -1,
        'userInfo': {'key': const.API_KEY, 'userId': device_id}
    }

    cipher_handler = CipherHandler(timestamp)
    data = cipher_handler.encrypt(json.dumps(data))

    post_data = {
        'data': data,
        'key': const.API_KEY,
        'timestamp': timestamp
    }

    resp = requests.post(url=const.OLD_API_URL, data=json.dumps(post_data))
    return resp.text


if __name__ == '__main__':
    ret = test()
    print(ret)
