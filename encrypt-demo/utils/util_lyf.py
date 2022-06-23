# coding=UTF-8
"""
pip install pycryptodome
"""
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode


class EncryptHandler(object):
    """
    加解密算法：AES
    加密模式：CBC
    填充：PKCS5Padding
    """

    def __init__(self, api_key, secret, timestamp):
        self.white_list = {
            'api_key_test': 'secret_test',
        }

        self.api_key = api_key
        self.secret = secret
        self.timestamp = timestamp
        self.secret_key = self.turn_secret_key()
        self.iv = self.secret_key
        self.block_size = AES.block_size
        self.mode = AES.MODE_CBC

    def turn_secret_key(self):
        if self.white_list.get(self.api_key) != self.secret:
            raise Exception("账号无效")
        else:
            return self.turn_hexdigest_md5(self.secret + str(self.timestamp) + self.api_key)

    @staticmethod
    def turn_hexdigest_md5(s):
        """
        md5加密
        """
        bt_input = bytearray(s, encoding='utf-8')

        md5 = hashlib.md5()
        md5.update(bt_input)
        return md5.hexdigest()

    @staticmethod
    def turn_digest_md5(s):
        """
        md5加密
        """
        bt_input = bytearray(s, encoding='utf-8')

        md5 = hashlib.md5()
        md5.update(bt_input)
        return md5.digest()

    def pad(self, text):
        """
        PKCS5Padding补位
        """
        return text + (self.block_size - len(text.encode()) % self.block_size) * chr(
            self.block_size - len(text.encode()) % self.block_size)

    @staticmethod
    def un_pad(text):
        """
        去除补位
        """
        return text[:-ord(text[len(text) - 1:])]

    def encrypt(self, text):
        """
        加密
        """
        text = self.pad(text).encode()
        key = self.turn_digest_md5(self.secret_key)
        IV = bytes(16)
        cipher = AES.new(key=key, mode=self.mode, IV=IV)
        encrypted_text = cipher.encrypt(text)
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        """
        解密
        """
        encrypted_text = b64decode(encrypted_text)
        key = self.turn_digest_md5(self.secret_key)
        IV = bytes(16)
        cipher = AES.new(key=key, mode=self.mode, IV=IV)
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.un_pad(decrypted_text).decode('utf-8')


if __name__ == '__main__':
    encrypt_handler = EncryptHandler('api_key_test', 'secret_test', 123456789)
    ret = encrypt_handler.encrypt('加密测试lyf')
    print(ret)

    ret_2 = encrypt_handler.decrypt(ret)
    print(ret_2)
# u960eSagaWESFhhQGUWWDw==
# u960eSagaWESFhhQGUWWDw==
