"""
@Author  :   luoyafei
@Time    :   2022/09/22 15:53:53
@Desc    :   None
"""

import os
import sys
import time
import click
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.config import dictConfig

log_path = 'D:\\CodePy\\tool-demos\\logs'


class MyselfLogHandler(logging.StreamHandler):
    """
    自定义的日志模块: 比如邮件模块、钉钉消息
    """

    def emit(self, record):
        request_id = record.request_id
        message = record.message
        print(f"===== 自定义的日志模块: {request_id} {message} =====")
        print(f"===== 自定义的日志模块: {record} =====")


class CustomFormatter(logging.Formatter):

    def format(self, record):
        try:
            request_id = "222333444"
        except Exception:
            request_id = ''
        record.request_id = request_id

        result = super().format(record)
        return result


TRACE_LOG_LEVEL = 5


class ColourizedFormatter(logging.Formatter):
    """
    A custom log formatter class that:

    * Outputs the LOG_LEVEL with an appropriate color.
    * If a log call includes an `extras={"color_message": ...}` it will be used
      for formatting the output, instead of the plain text message.
    """

    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(str(level_name), fg="blue"),
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red"
        ),
    }

    def __init__(self, fmt=None, datefmt=None, style="%", use_colors=None):
        if use_colors in (True, False):
            self.use_colors = use_colors
        else:
            self.use_colors = sys.stdout.isatty()
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name, level_no):
        def default(level_name): return str(level_name)

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def should_use_colors(self):
        return True

    def formatMessage(self, record):
        try:
            request_id = "222333444"
        except Exception:
            request_id = ''
        record.request_id = request_id
        levelname = record.levelname
        seperator = " " * (8 - len(record.levelname))
        if self.use_colors:
            levelname = self.color_level_name(levelname, record.levelno)
            if "color_message" in record.__dict__:
                record.msg = record.__dict__["color_message"]
                record.__dict__["message"] = record.getMessage()
        record.__dict__["levelprefix"] = levelname + ":" + seperator
        return super().formatMessage(record)


class DefaultFormatter(ColourizedFormatter):
    def should_use_colors(self):
        return sys.stderr.isatty()


class FilterLevel(object):
    def __init__(self, level_name):
        self.level_name = level_name

    def filter(self, record):
        if record.levelname < self.level_name:
            return False
        else:
            return True


# 多进程安全
class ProcessSaveTimeFileHandler(TimedRotatingFileHandler):

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False,
                 atTime=None):
        self.when = when.upper()

        if self.when == 'S':
            self.suffix = "%Y-%m-%d_%H-%M-%S"
        elif self.when == 'M':
            self.suffix = "%Y-%m-%d_%H-%M"
        elif self.when == 'H':
            self.suffix = "%Y-%m-%d_%H"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.suffix = "%Y-%m-%d"
        elif self.when.startswith('W'):
            if len(self.when) != 2:
                raise ValueError("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s" % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError("Invalid day specified for weekly rollover: %s" % self.when)
            self.suffix = "%Y-%m-%d"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.prefix_name = filename
        baseFilename = self.prefix_name + '-' + time.strftime(self.suffix, time.localtime(time.time())) + ".log"
        super().__init__(filename=baseFilename, when=when, interval=interval, backupCount=backupCount,
                         encoding=encoding, delay=delay, utc=utc, atTime=atTime)

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        # self.baseFilename = self.prefix_name + '-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".log"

        self.baseFilename = self.rotation_filename(self.prefix_name + "-" +
                                                   time.strftime(self.suffix, time.localtime(time.time())) + ".log")
        # if os.path.exists(dfn):
        #     os.remove(dfn)
        # self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName.split('-')[0]
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                # suffix = fileName.split('.')[0]
                suffix = fileName[plen + 1:].split('.')[0]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result


def set_logger_config(file_name):
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        'incremental': False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(filename)s - %(lineno)d - %(request_id)s - %(levelname)s - %(message)s",
                "()": "utils.util_logger.CustomFormatter"
            },
            "console": {
                "()": "utils.util_logger.DefaultFormatter",
                "fmt": "%(asctime)s - %(filename)s - %(lineno)d - %(request_id)s - %(levelprefix)s - %(levelname)s - %(message)s",
                "use_colors": None,
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "utils.util_logger.ProcessSaveTimeFileHandler",
                "when": "MIDNIGHT",
                "backupCount": 14,
                "level": logging.INFO,
                "filename": os.path.join(log_path, file_name)
            },
            "console": {
                "formatter": "console",
                "class": "logging.StreamHandler",
                "level": logging.DEBUG
            },
            "error": {
                "()": "utils.util_logger.ProcessSaveTimeFileHandler",
                "level": logging.ERROR,
                "formatter": "default",
                "when": "MIDNIGHT",
                "backupCount": 14,
                "filename": os.path.join(log_path, f'{file_name}-error'),
            },
            "myself": {
                "()": "utils.util_logger.MyselfLogHandler",
                "level": logging.ERROR,
                "formatter": "default",
            }
        },
        "loggers": {
            "": {
                "handlers": ["default", "console"],
                "level": logging.DEBUG
            },
            "server": {
                "handlers": ["default", "console", "error", "myself"],
                "level": logging.DEBUG,
                "propagate": False
            },
            "databases": {
                "handlers": ["default"],
                "level": logging.DEBUG
            }
        }
    }

    dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    set_logger_config("test")
    logger = logging.getLogger("server")

    logger.info("test info message")
    logger.error("test error message")
