"""
单例
"""


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            return cls._instance


s1 = Singleton()
s2 = Singleton()
print(s1)  # <__main__.Singleton object at 0x000002223BBDB278>
print(s2)  # <__main__.Singleton object at 0x000002223BBDB278>
