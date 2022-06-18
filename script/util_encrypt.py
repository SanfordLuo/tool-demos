"""
pip install pycryptodome
"""
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

default_iv = bytes(16)
block_size = AES.block_size
mode = AES.MODE_CBC


class CipherHandler(object):

    def __init__(self, api_key, secret, timestamp, iv=None):
        self.api_key = api_key
        self.secret = secret
        self.timestamp = timestamp
        self.iv = iv

    @staticmethod
    def md5_hexdigest(s: str) -> str:
        bt_input = bytearray(s, encoding='utf-8')
        md5_inst = hashlib.md5()
        md5_inst.update(bt_input)
        return md5_inst.hexdigest()

    @staticmethod
    def md5_digest(s: str) -> bytes:
        bt_input = bytearray(s, encoding='utf-8')
        md5_inst = hashlib.md5()
        md5_inst.update(bt_input)
        return md5_inst.digest()

    @staticmethod
    def pad(text):
        """
        PKCS5Padding补位
        """
        return text + (block_size - len(text.encode()) % block_size) * chr(block_size - len(text.encode()) % block_size)

    @staticmethod
    def un_pad(text):
        """
        去除补位
        """
        return text[:-ord(text[len(text) - 1:])]

    @property
    def aes_key(self):
        secret_key = self.secret + str(self.timestamp) + self.api_key
        return self.md5_hexdigest(secret_key)

    @property
    def cipher(self):
        key = self.md5_digest(self.aes_key)
        iv = self.iv.encode() if self.iv else default_iv
        return AES.new(key=key, mode=mode, IV=iv)

    def encrypt(self, text):
        text = self.pad(text).encode()
        encrypted_text = self.cipher.encrypt(text)
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, text):
        text = b64decode(text)
        decrypted_text = self.cipher.decrypt(text)
        return self.un_pad(decrypted_text).decode('utf-8')


if __name__ == '__main__':
    cipher_handler = CipherHandler('api_key_test', 'secret_test', '123456789123456789')
    ret = cipher_handler.encrypt('加密测试')
    print(ret)

    ret2 = cipher_handler.decrypt(ret)
    print(ret2)
