import hashlib


def md5_hexdigest(s: str) -> str:
    bt_input = bytearray(s, encoding='utf-8')
    md5_inst = hashlib.md5()
    md5_inst.update(bt_input)
    return md5_inst.hexdigest()


def md5_digest(s: str) -> bytes:
    bt_input = bytearray(s, encoding='utf-8')
    md5_inst = hashlib.md5()
    md5_inst.update(bt_input)
    return md5_inst.digest()
