import traceback
from script import log_handler

logger = log_handler.Logger('test_log_handler.log').logger


def test_00():
    logger.info("测试 log handler")

    ret = 0
    try:
        ret = 2 / 0
        logger.info("测试info级别")
    except Exception:
        logger.error("测试error级别, err: {}".format(traceback.format_exc()))

    try:
        ret = 2 / 2
        logger.info("测试info级别")
    except Exception:
        logger.error("测试error级别, err: {}".format(traceback.format_exc()))

    return ret


if __name__ == '__main__':
    test_00()
