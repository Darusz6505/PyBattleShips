import time
import asyncio

import websockets


class Server:

    async def echo(self, websocket, path):
        try:
            async for message in websocket:
                print(message)
                await websocket.send(message)


        except RuntimeError:
            print("Error")


s = Server()

asyncio.get_event_loop().run_until_complete(

    websockets.serve(s.echo, 'localhost', 8765)
)
asyncio.get_event_loop().run_forever()

