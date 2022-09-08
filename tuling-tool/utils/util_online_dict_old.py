import time
import json
import random
import websockets
import logging
from utils import const
from utils.util_encrypt import CipherHandler

logger = logging.getLogger("server")


class OnlineDictHandler(object):
    def __init__(self, dict_type, dict_dicts):
        self.dict_type = dict_type
        self.dict_dicts = dict_dicts

        self.device_ids = const.WS_DEVICE_IDS
        self.device_idx = random.randint(0, len(self.device_ids)-1)

        self.min_limit = []
        self.hour_limit = []
        self.day_limit = []
        self.min_sleep = 30
        self.hour_sleep = 300
        self.day_sleep = 3000

    def __validator_params(self):
        if not isinstance(self.dict_type, str):
            raise Exception(f'{self.dict_type} is invalid dict type.')
        if not isinstance(self.dict_dicts, list):
            raise Exception(f'{self.dict_dicts} is invalid dict dicts.')

        if self.dict_type not in [const.TULING_DICT, const.NIUJIN_DICT]:
            raise Exception(f'{self.dict_type} is invalid dict type.')
        for dict_dict in self.dict_dicts:
            if dict_dict not in const.DICT_DICTS:
                raise Exception(f'{dict_dict} is invalid dict dicts.')

    def __format_req_data(self, text):
        timestamp = str(int(time.time() * 1000))
        data = {
            "deviceId": self.device_ids[self.device_idx],
            "requestType": ["NLP"],
            "nlpRequest": {
                "content": [{
                    "data": text
                }],
                "clientInfo": {
                    "appState": {
                        "code": 1000633,
                        "operateState": 1100
                    },
                    "robotSkill": {
                        "1000633": {
                            "dictType": self.dict_type,
                            "dicts": self.dict_dicts
                        }
                    }
                }
            }
        }

        cipher_handler = CipherHandler(timestamp, req_type="ws")
        data = cipher_handler.encrypt(json.dumps(data))

        req_data = {
            'data': data,
            'key': const.WS_KEY,
            'timestamp': timestamp
        }
        self.req_data = json.dumps(req_data)

    async def translate(self, text):
        self.__validator_params()
        self.__format_req_data(text)

        try:
            async with websockets.connect(const.WS_URL) as ws:
                logger.info(f"ws send: {text}")
                await ws.send(self.req_data)
                while True:
                    resp_text = await ws.recv()
                    logger.info(f"ws recv: {resp_text}")

                    resp_code = json.loads(resp_text)['code']

                    if resp_code == 200:
                        self.min_limit = []
                        self.hour_limit = []
                        self.day_limit = []
                        await ws.close()
                        return resp_text

                    if resp_code in [4012, 4013, 4014, 4200]:
                        if resp_code == 4012:
                            # 每天限制
                            self.day_limit.append(self.device_ids[self.device_idx])
                            if len(set(self.day_limit)) >= len(self.device_ids):
                                logger.error(f"每天限制: {self.day_limit}, 开始睡眠: {self.day_sleep}")
                                time.sleep(self.day_sleep)
                                self.day_limit = []

                        if resp_code in [4013, 4012]:
                            # 每小时限制
                            self.hour_limit.append(self.device_ids[self.device_idx])
                            if len(set(self.hour_limit)) >= len(self.device_ids):
                                logger.error(f"每小时限制: {self.hour_limit}, 开始睡眠: {self.hour_sleep}")
                                time.sleep(self.hour_sleep)
                                self.hour_limit = []

                        if resp_code in [4014, 4013, 4012]:
                            # 每分钟限制
                            self.min_limit.append(self.device_ids[self.device_idx])
                            if len(set(self.min_limit)) >= len(self.device_ids):
                                logger.error(f"每分钟限制: {self.min_limit}, 开始睡眠: {self.min_sleep}")
                                time.sleep(self.min_sleep)
                                self.min_limit = []

                        if self.device_idx < len(self.device_ids) - 1:
                            self.device_idx += 1
                        else:
                            self.device_idx = 0

                        time.sleep(1)
                        await ws.close()
                        raise Exception(f"{self.device_ids[self.device_idx]}: {resp_text}")

        except Exception as e:
            logger.error(f"ws error: {e}")
            return ""
