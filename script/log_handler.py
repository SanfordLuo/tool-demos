"""
日志处理器
"""
import os
import flask
import logging
from logging.handlers import TimedRotatingFileHandler
# from config import config
path = "D:\\CodePy\\tool-demos"

class LogFormatter(logging.Formatter):

    @property
    def request_id(self):
        try:
            request_id = flask.request.headers.get('request_id')
        except Exception:
            request_id = ''
        return request_id

    def format(self, record):
        record.request_id = self.request_id
        result = super().format(record)
        return result


class Logger(object):
    def __init__(self, filename=None):
        if not filename:
            filename = 'main.log'
        if os.path.exists(path):
            if not os.path.exists(f'{path}/logs'):
                os.mkdir(f'{path}/logs')
            filename = f'{path}/logs/{filename}'
        else:
            project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if not os.path.exists(f'{project_path}/logs'):
                os.mkdir(f'{project_path}/logs')
            filename = f'{project_path}/logs/{filename}'

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.formatter = LogFormatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(request_id)s] %(message)s')

        self.file_handler = TimedRotatingFileHandler(filename, when='MIDNIGHT', interval=1, backupCount=7)
        self.file_handler.setLevel(logging.INFO)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
