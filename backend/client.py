import asyncio
import json
import sys
import time

import websockets

from message import AttackMessage, BaseMessage

# message = sys.argv[1]
message = AttackMessage(x=sys.argv[1], y=sys.argv[2])

def handleAttack(msg : AttackMessage):
    print("I've been hit ", msg.x, msg.y)


async def hello():
    # "ws://localhost:8765" - muszą być apostofy podwójne !
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocekt:
        try:
            while True:
                now = time.strftime("%X")
                print("Sending: ", now, message.toJSON())
                await websocekt.send(message.toJSON())
                msg = await websocekt.recv()
                print("Received: ", msg)
                # rozłączenie się partnera z gry
                msg = BaseMessage(data=json.loads(msg))
                if msg.type == BaseMessage.PLAYER_DISCONNECTED:
                    print(BaseMessage.PLAYER_DISCONNECTED)
                    await websocekt.close()
                    break
                elif msg.type == BaseMessage.ATTACK:
                    handleAttack(msg)


        except websockets.excpetions.connectionClosed as ex:
            print(ex)


asyncio.get_event_loop().run_until_complete(hello())

