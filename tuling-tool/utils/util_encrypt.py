"""
pip install pycryptodome
"""
import hashlib
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
from utils import const


class CipherHandler(object):

    def __init__(self, timestamp, req_type="api"):
        self.req_type = req_type
        self.timestamp = timestamp
        self.default_iv = bytes(16)
        self.block_size = AES.block_size
        self.mode = AES.MODE_CBC

    def __md5_hexdigest(self, s_input: str) -> str:
        bt_input = bytearray(s_input, encoding="utf-8")
        md5_inst = hashlib.md5()
        md5_inst.update(bt_input)
        return md5_inst.hexdigest()

    def __md5_digest(self, s_input: str) -> bytes:
        bt_input = bytearray(s_input, encoding="utf-8")
        md5_inst = hashlib.md5()
        md5_inst.update(bt_input)
        return md5_inst.digest()

    def __pad(self, text: str) -> str:
        """
        PKCS5Padding补位
        """
        return text + (self.block_size - len(text.encode()) % self.block_size) * chr(
            self.block_size - len(text.encode()) % self.block_size)

    def __unpad(self, text: str) -> bytes:
        """
        去除补位
        """
        return text[:-ord(text[len(text) - 1:])]

    @property
    def __cipher(self):
        if self.req_type == "ws":
            secret_key = const.WS_KEY + const.WS_SECRET + str(self.timestamp)
            key = self.__md5_hexdigest(secret_key)[8:-8].encode()
            iv = key

        else:
            secret_key = const.API_SECRET + str(self.timestamp) + const.API_KEY
            key = self.__md5_digest(self.__md5_hexdigest(secret_key))
            iv = self.default_iv

        return AES.new(key=key, mode=self.mode, IV=iv)

    def encrypt(self, text: str) -> str:
        text = self.__pad(text).encode()
        encrypted_text = self.__cipher.encrypt(text)
        return b64encode(encrypted_text).decode("utf-8")

    def decrypt(self, text: str) -> str:
        text = b64decode(text)
        decrypted_text = self.__cipher.decrypt(text)
        return self.__unpad(decrypted_text).decode("utf-8")


if __name__ == '__main__':
    cipher_handler = CipherHandler(timestamp="111222333444")
    ret = cipher_handler.encrypt("加密测试")
    print(ret)

    ret2 = cipher_handler.decrypt(ret)
    print(ret2)
