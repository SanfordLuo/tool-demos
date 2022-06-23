# coding=UTF-8
"""
pip install pycryptodome
"""
from Crypto.Cipher import AES
from util_md5 import md5_digest
from base64 import b64decode, b64encode

default_iv = bytes(16)
block_size = AES.block_size
mode = AES.MODE_CBC


class CipherHandler(object):

    def __init__(self, aes_key, iv=None):
        self.aes_key = aes_key
        self.iv = iv

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
    def cipher(self):
        key = md5_digest(self.aes_key)
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
