import grpc
import json
import time
import random
import music_pb2
import music_pb2_grpc
from concurrent import futures


class MusicServer(music_pb2_grpc.MusicServicer):
    def __init__(self):
        with open('test_data.json', 'r') as f:
            data = json.load(f)
        self.music_data = data['music']

    def get_music(self, request, context):
        """
        简单模式, 根据歌名查找对应歌曲信息
        """
        name = request.name
        ret = [_ for _ in self.music_data if _['name'] == name]
        if ret:
            ret = ret[0]
            return music_pb2.music_resp(name=ret['name'], singer=ret['singer'], ranking=ret['ranking'])
        else:
            return music_pb2.music_resp(message='未查到对应歌曲')

    def ranking_music(self, request, context):
        """
        服务端流模式, 每隔3秒随机返回一首歌曲
        """
        limit = request.limit
        for i in range(limit):
            ret = random.choice(self.music_data)
            feature = music_pb2.ranking_resp(data=ret)
            time.sleep(3)

            # 依迭代器的方式返回处理结果
            yield feature


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    music_pb2_grpc.add_MusicServicer_to_server(MusicServer(), server)
    server.add_insecure_port('127.0.0.1:7779')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()
