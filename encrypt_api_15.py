from utils.util_encrypt import CipherHandler
import requests
import time
import json

api_key = '9079fd6661f14c9ebb2544694cdca205'
secret = '70z99c84Ma5Eo3UT'
device_id = "u1112223"

url = "http://api.turingos.cn/turingosapi"


def test():
    timestamp = str(int(time.time() * 1000))
    data = {
        'perception': {'audition': {'text': '你好'}},
        'reqType': -1,
        'userInfo': {'key': api_key, 'userId': device_id}
    }

    # cipher_handler = CipherHandler(api_key, secret, timestamp)
    # data = cipher_handler.encrypt(json.dumps(data))

    post_data = {
        'data': data,
        'key': api_key,
        'timestamp': timestamp
    }

    resp = requests.post(url=url, data=json.dumps(post_data))
    return resp.text


if __name__ == '__main__':
    ret = test()
    print(ret)
