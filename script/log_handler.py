"""
日志处理器
"""
import os
import logging
from logging.handlers import RotatingFileHandler

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = "{}/log/".format(PROJECT_PATH)


class Logger(object):
    def __init__(self, logname):
        if not os.path.isdir(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.logger = logging.getLogger()
        self.formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 多线程安全，多进程不安全
        self.handler = RotatingFileHandler(
            filename=LOG_DIR + os.sep + logname,
            maxBytes=200 * 1024 * 1024,
            backupCount=5,
            mode="a",
            encoding="utf-8")
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def set_my_level_info(self):
        self.logger.setLevel(logging.INFO)

    def set_my_level_warning(self):
        self.logger.setLevel(logging.WARNING)


if __name__ == "__main__":
    logger = Logger("service.log")
