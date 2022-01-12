"""
自省函数
自省是一种对象自我检查的能力: 检查自己有什么属性、有什么方法
自省的更高级的机制也就是反射: 可以动态的给自己添加函数、属性
"""


class TestA:
    def __init__(self):
        self.name = 'sanford'
        self.age = 26

    def test_a(self):
        return "aaa"

    def test_b(self):
        return "bbb"


class Run:
    def __init__(self):
        self.class_test_a = TestA()
        self.ret_hasattr = None
        self.ret_getattr = None
        self.isinstance = None

    def test_hasattr(self):
        """
        判断某个类实例对象是否包含指定名称的属性或方法, 返回bool值
        :return:
        """
        self.ret_hasattr = [hasattr(self.class_test_a, "name"), hasattr(self.class_test_a, "time"),
                            hasattr(self.class_test_a, "test_a")]
        return self.ret_hasattr

    def test_getattr(self):
        """
        获取某个类实例对象中指定属性的值, 如果没有则返回默认值或报错
        :return:
        """
        self.ret_getattr = [getattr(self.class_test_a, "name"), getattr(self.class_test_a, "test_a"),
                            getattr(self.class_test_a, "default", None)]
        return self.ret_getattr

    def test_setattr(self):
        """
        修改类实例对象中的属性值, 它还可以实现为实例对象动态添加属性或者方法
        :return:
        """
        setattr(self.class_test_a, "email", "86@qq.com")
        setattr(self.class_test_a, "age", "99")
        setattr(self.class_test_a, "test_a", self.class_test_a.test_b)
        return self.class_test_a.email, self.class_test_a.age, self.class_test_a.test_a()

    def test_isinstance(self):
        """
        用于判断变量类型
        :return:
        """
        self.isinstance = [isinstance("test_str", str), isinstance("test_str", (str, int)), isinstance(222, str)]
        return self.isinstance


if __name__ == '__main__':
    run = Run()
    ret_hasattr = run.test_hasattr()
    print(ret_hasattr)

    ret_getattr = run.test_getattr()
    print(ret_getattr)

    email, age, test_a = run.test_setattr()
    print(email, age, test_a)

    ret_isinstance = run.test_isinstance()
    print(ret_isinstance)
