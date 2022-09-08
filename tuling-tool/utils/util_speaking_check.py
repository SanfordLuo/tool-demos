import os
import time
import json
import random
import websockets
import logging
from pydub import AudioSegment
from utils import const
from utils.util_encrypt import CipherHandler

logger = logging.getLogger("server")


class SpeakingCheckHandler(object):
    def __init__(self, checking_type, device_id=None):
        self.checking_type = checking_type
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

    async def __init_req(self, ws, text, file_uuid):
        """
        mp3格式: channel=2, sampleRate=16000, sampleBytes=2
        wav格式: channel=1, sampleRate=16000, sampleBytes=2
        """
        timestamp = str(int(time.time() * 1000))
        data = {
            "deviceId": self.using_device_id,
            "requestType": [1],
            "nlpRequest": {
                "content": [{
                    "type": 5,
                    "data": file_uuid,
                    "binaryDetail": {
                        "name": text,
                        "type": "wav",
                        "ext": {
                            "channel": 1,
                            "sampleRate": 16000,
                            "sampleBytes": 2
                        }
                    }
                }],
                "clientInfo": {
                    "appState": {
                        "code": 1000047,
                        "operateState": self.checking_type
                    }
                }
            },
            "binarysState": {
                "openBinarysId": file_uuid
            }
        }

        logger.info(f"init_req: {data}")

        cipher_handler = CipherHandler(timestamp, req_type="ws")
        data = cipher_handler.encrypt(json.dumps(data))

        init_data = {
            'data': data,
            'key': const.WS_KEY,
            'timestamp': timestamp
        }
        await ws.send(json.dumps(init_data))

    async def __file_req(self, ws, file_path):
        """
        -ab bitrate 设置音频码率
        -ar freq 设置音频采样率
        -ac channels 设置通道
        """
        audio = AudioSegment.from_file(file_path, file_path.split(".")[-1])
        new_file_path = ".".join(file_path.split(".")[:-1])+".wav"
        audio.export(new_file_path, format="wav", parameters=["-ac", "1", "-ar", "16000", "-ab", "16"])

        file_data = []
        with open(new_file_path, "rb") as f:
            while True:
                data = f.read(1024*8)
                if data:
                    file_data.append(data)
                else:
                    break

        os.remove(new_file_path)

        logger.info(f"file_req times: {len(file_data)}")

        for _data in file_data:
            await ws.send(_data)

    async def __end_req(self, ws, file_uuid):
        timestamp = str(int(time.time() * 1000))
        data = {
            "binarysState": {
                "completeBinarysId": file_uuid
            }
        }

        logger.info(f"end_req: {data}")

        cipher_handler = CipherHandler(timestamp, req_type="ws")
        data = cipher_handler.encrypt(json.dumps(data))

        end_data = {
            'data': data,
            'key': const.WS_KEY,
            'timestamp': timestamp
        }
        await ws.send(json.dumps(end_data))

    async def checking(self, text, file_uuid, file_path):
        try:
            async with websockets.connect(const.WS_URL) as ws:

                logger.info(f"ws send: {text}, {file_uuid}, {file_path}")
                await self.__init_req(ws, text, file_uuid)

                while True:
                    resp_text = await ws.recv()
                    logger.info(f"ws recv: {resp_text}")

                    resp_code = json.loads(resp_text)['code']

                    if resp_code == 210:
                        await self.__file_req(ws, file_path)
                        await self.__end_req(ws, file_uuid)

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
