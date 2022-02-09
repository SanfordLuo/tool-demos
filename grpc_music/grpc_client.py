import grpc
import music_pb2
import music_pb2_grpc


def get_music(stub, name):
    """
    简单模式, 根据歌名查找对应歌曲信息
    """
    resp = stub.get_music(music_pb2.name_req(name=name))
    if not resp.message:
        ret_data = dict(
            name=resp.name,
            singer=resp.singer,
            ranking=resp.ranking
        )
    else:
        ret_data = dict(
            message=resp.message
        )
    print(ret_data)


def ranking_music(stub, limit):
    """
    服务端流模式, 每隔3秒随机返回一首歌曲
    """
    features = stub.ranking_music(music_pb2.limit_req(limit=limit))
    for feature in features:
        ret_data = dict(
            name=feature.data.name,
            singer=feature.data.singer,
            ranking=feature.data.ranking
        )
        print(ret_data)


def run():
    with grpc.insecure_channel('127.0.0.1:7779') as channel:
        stub = music_pb2_grpc.MusicStub(channel=channel)

        # get_music(stub, name='鞋子特大号')
        # get_music(stub, name='哈哈哈')

        ranking_music(stub, limit=10)


if __name__ == '__main__':
    run()
