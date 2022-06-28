import asyncio
import websockets


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello world!")
        recv_text = await websocket.recv()
        print(recv_text)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello('ws://localhost:8765'))
