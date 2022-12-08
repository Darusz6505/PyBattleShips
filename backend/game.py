
import asyncio
import json
import time
from message import BaseMessage

from message import PlayerDisconnectedMesage


class Game:
    players = []
    lastActivity = time.time()

    def __init__(self):
        self.players = []
        self.lastActivity = time.time()

    def add_player(self, websocket):
        self.players.append(websocket)

    async def handle(self, websocket, message):
        self.lastActivity = time.time()
        message = BaseMessage(data=json.loads(message))

        if message.type == BaseMessage.PLAYER_DISCONNECTED:
            await self.sendBoth(message.toJSON())

        if len(self.players) == 2:
            await self.sendToOther(websocket, message.toJSON())


    async def timeout(self):
        for player in self.players:
            await player.send("Timeout")

    async def sendBoth(self, message):
        for player in self.players:
            await player.send(message)

    async def sendToOther(self, websocket, message):
        for player in self.players:
            if player == websocket:
                continue
            # await asyncio.sleep(0.5)
            await player.send(message)

    async def handleDisconnect(self, websocket):
        if self.players == 1:
            return
        await self.sendToOther(websocket, PlayerDisconnectedMesage().toJSON())
        if self.players[0] == websocket:
            del self.players[0]
        else:
            del self.players[1]