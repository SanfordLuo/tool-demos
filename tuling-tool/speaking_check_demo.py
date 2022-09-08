import os
import uuid
import asyncio
import logging
from utils.util_speaking_check import SpeakingCheckHandler
from utils import util_logger
from utils import const

log_name = os.path.basename(__file__).split(".")[0]
util_logger.set_logger_config(log_name)
logger = logging.getLogger(log_name)

device_id = const.WS_DEVICE_IDS[0]
checking_type = const.SPEAKING_EN_WORD
file_uuid = ''.join(str(uuid.uuid4()).split('-'))
file_path = "D:\\CodeOkay\\tuling-tool\\data\\audio\\20220712_hello.m4a"
text = "hello"


async def run_checking():
    speaking_check_handler = SpeakingCheckHandler(checking_type, device_id)
    ret_text = await speaking_check_handler.checking(text, file_uuid, file_path)
    print(ret_text)

if __name__ == '__main__':
    asyncio.run(run_checking())
