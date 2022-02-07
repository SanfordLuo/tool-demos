from xmlrpc import client
import zerorpc


def test_xmlrpc():
    server = client.ServerProxy("http://localhost:7777")
    print(server.get_songs())
    print(server.get_songs(1))

    server.add_song('晴天')
    print(server.get_songs())

    server.delete_song('七里香')
    print(server.get_songs())


def test_zerorpc():
    client = zerorpc.Client()
    client.connect('tcp://127.0.0.1:7778')

    print(client.get_songs())
    print(client.get_songs(1))

    client.add_song('晴天')
    print(client.get_songs())

    client.delete_song('七里香')
    print(client.get_songs())


if __name__ == '__main__':
    # test_xmlrpc()

    test_zerorpc()
