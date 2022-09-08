import time
import json
import random
import websockets
import logging
from utils import const
from utils.util_encrypt import CipherHandler

logger = logging.getLogger("server")


class OnlineDictHandler(object):
    def __init__(self, dict_type, dict_dicts, device_id=None):
        self.dict_type = dict_type
        self.dict_dicts = dict_dicts
        self.device_id = device_id
        self.device_idx = -1

        self.min_limit = []
        self.hour_limit = []
        self.day_limit = []

    @property
    def using_device_id(self):
        if self.device_id in const.WS_DEVICE_IDS and self.device_idx == -1:
            return self.device_id
        else:
            if self.device_idx == -1:
                self.device_idx = random.randint(0, len(const.WS_DEVICE_IDS)-1)
            return const.WS_DEVICE_IDS[self.device_idx]

    async def __data_req(self, ws, text):
        timestamp = str(int(time.time() * 1000))
        data = {
            "deviceId": self.using_device_id,
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

        logger.info(f"data_req: {data}")

        cipher_handler = CipherHandler(timestamp, req_type="ws")
        data = cipher_handler.encrypt(json.dumps(data))

        req_data = {
            'data': data,
            'key': const.WS_KEY,
            'timestamp': timestamp
        }
        await ws.send(json.dumps(req_data))

    async def translate(self, text):
        try:
            async with websockets.connect(const.WS_URL) as ws:

                logger.info(f"ws send: {text}")
                await self.__data_req(ws, text)

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
                            self.day_limit.append(self.using_device_id)
                            if len(set(self.day_limit)) >= len(const.WS_DEVICE_IDS):
                                logger.error(f"每天限制: {set(self.day_limit)}, 开始睡眠: {const.LIMIT_DAY_SLEEP}")
                                time.sleep(const.LIMIT_DAY_SLEEP)
                                self.day_limit = []

                        if resp_code in [4013, 4012]:
                            # 每小时限制
                            self.hour_limit.append(self.using_device_id)
                            if len(set(self.hour_limit)) >= len(const.WS_DEVICE_IDS):
                                logger.error(f"每小时限制: {set(self.hour_limit)}, 开始睡眠: {const.LIMIT_HOUR_SLEEP}")
                                time.sleep(const.LIMIT_HOUR_SLEEP)
                                self.hour_limit = []

                        if resp_code in [4014, 4013, 4012]:
                            # 每分钟限制
                            self.min_limit.append(self.using_device_id)
                            if len(set(self.min_limit)) >= len(const.WS_DEVICE_IDS):
                                logger.error(f"每分钟限制: {set(self.min_limit)}, 开始睡眠: {const.LIMIT_MIN_SLEEP}")
                                time.sleep(const.LIMIT_MIN_SLEEP)
                                self.min_limit = []

                        if self.device_idx < len(const.WS_DEVICE_IDS) - 1:
                            self.device_idx += 1
                        else:
                            self.device_idx = 0

                        await ws.close()
                        raise Exception(f"{self.using_device_id}: {resp_text}")

        except Exception as e:
            logger.error(f"ws error: {e}")
            return ""
