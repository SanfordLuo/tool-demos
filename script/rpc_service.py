from xmlrpc.server import SimpleXMLRPCServer
import zerorpc


class SongHandler(object):

    def __init__(self):
        self.songs = ['七里香', '以父之名', '夜曲', '夜的第七章']

    def add_song(self, song):
        if song not in self.songs:
            self.songs.append(song)

    def delete_song(self, song):
        if song in self.songs:
            self.songs.remove(song)

    def get_songs(self, idx=None):
        try:
            return self.songs[idx]
        except Exception:
            return self.songs


def run_xmlrpc():
    song_handler = SongHandler()
    server = SimpleXMLRPCServer(('localhost', 7777), allow_none=True)
    server.register_instance(song_handler)
    server.serve_forever()


def run_zerorpc():
    song_handler = SongHandler()
    server = zerorpc.Server(song_handler)
    server.bind('tcp://127.0.0.1:7778')
    server.run()


if __name__ == '__main__':
    # run_xmlrpc()

    run_zerorpc()
