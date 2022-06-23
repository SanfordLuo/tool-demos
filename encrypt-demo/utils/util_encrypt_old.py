from util_md5 import md5_hexdigest
from util_aes import CipherHandler


def cipher_handler(api_key, secret, timestamp):
    secret_key = secret + str(timestamp) + api_key
    aes_key = md5_hexdigest(secret_key)
    return CipherHandler(aes_key)


def encrypt(text, api_key, secret, timestamp):
    ma = cipher_handler(api_key, secret, timestamp)
    return ma.encrypt(text)


def decrypt(text, api_key, secret, timestamp):
    ma = cipher_handler(api_key, secret, timestamp)
    return ma.decrypt(text)


if __name__ == '__main__':
    ret = encrypt('加密测试', 'api_key_test', 'secret_test', '123456789123456789')
    print(ret)

    ret2 = decrypt(ret, 'api_key_test', 'secret_test', '123456789123456789')
    print(ret2)
