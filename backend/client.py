import asyncio
import sys
import time

import websockets

message = sys.argv[1]


async def hello():
    # "ws://localhost:8765" - muszą być apostofy podwójne !
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocekt:
        while True:
            now = time.strftime("%X")
            print("Sending: ", now, message)
            await websocekt.send(message)
            msg = await websocekt.recv()
            print("Received: ", msg)
            await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())

