import os
import asyncio
import logging
from utils.util_online_dict import OnlineDictHandler
from utils import util_logger
from utils import const

log_name = os.path.basename(__file__).split(".")[0]
util_logger.set_logger_config(log_name)
logger = logging.getLogger(log_name)

device_id = const.WS_DEVICE_IDS[0]
dict_type = const.TULING_DICT
dict_dicts = [const.DICT_EN_WORD]
text = "today"


async def run_translate():
    online_dict_handler = OnlineDictHandler(dict_type, dict_dicts, device_id)
    ret_text = await online_dict_handler.translate(text)
    print(ret_text)


if __name__ == '__main__':
    asyncio.run(run_translate())
