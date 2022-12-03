import asyncio
import sys
import time

import websockets

message = sys.argv[1]


async def hello():
    # "ws://localhost:8765" - muszą być apostofy podwójne !
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocekt:
        try:
            while True:
                now = time.strftime("%X")
                print("Sending: ", now, message)
                await websocekt.send(message)
                msg = await websocekt.recv()
                print("Received: ", msg)
                # rozłączenie się partnera z gry
                if msg == "Disconnect":
                    print(msg)
                    await websocekt.close()
                    break
        except websockets.excpetions.connectionClosed as ex:
            print(ex)


asyncio.get_event_loop().run_until_complete(hello())

