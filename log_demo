import logging

def mylog():
    logger = logging.getLogger('commlog')  # 不加名称设置root logger
    logger.setLevel(logging.DEBUG)
    """
    %(name)s Logger的名字
    setLevel: 指定日志的级别
    %(levelno)s 数字形式的日志级别
    %(levelname)s 文本形式的日志级别
    %(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
    %(filename)s 调用日志输出函数的模块的文件名
    %(module)s 调用日志输出函数的模块名
    %(funcName)s 调用日志输出函数的函数名
    %(lineno)d 调用日志输出函数的语句所在的代码行
    %(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
    %(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
    %(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
    %(thread)d 线程ID。可能没有
    %(threadName)s 线程名。可能没有
    %(process)d 进程ID。可能没有
    %(message)s 用户输出的消息
    """
    formatter = logging.Formatter('%(asctime)s [%(lineno)d] %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    # 使用FileHandler输出到文件
    fh = logging.FileHandler('test_log.log', encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 使用StreamHandler输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # 添加两个Handler
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger
