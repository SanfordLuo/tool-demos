class DemoMethod(object):
    name = "西瓜"

    def __init__(self, name):
        self.name = name

    def objMethod(self, other):
        print("%s是实例方法;%s" % (self.name, other))

    @classmethod
    def clsMethon(cls, other):
        print("%s是类方法, 只能调用类变量%s" % (cls.name, other))

    @staticmethod
    def staMethod(other):
        print("我是静态方法;%s" % other)

obj = DemoMethod("橙子")
obj.objMethod("hahah")
DemoMethod.clsMethon("jay")
DemoMethod.staMethod("chou")

# 橙子是实例方法;hahah
# 西瓜是类方法, 只能调用类变量jay
# 我是静态方法;chou
