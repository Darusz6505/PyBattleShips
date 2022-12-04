import asyncio
from kivy import Config
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from client import Client

import plane
from gamebutton import GameButton

from message import BaseMessage, PlayerConnectedMesage, SankMessage, HitMessage, MissMessage



class Battleships(GridLayout):
    

    def __init__(self, **kwargs):
        super(Battleships, self).__init__(**kwargs)
        self.isGameStarted = False
        self.client = Client(self.onMessage)
        self.ids['opponent'].disabled = True
        self.lastX = 0
        self.lastY = 0

        for c1 in self.children:
            for c2 in c1.children:
                for c3 in c2.children:
                    for c4 in c3.children:
                        if isinstance(c4, GameButton):
                            c4.sendMessage = self.sendMessage
                            c4.saveLastHitPosition = self.saveLastHitPosition

    def saveLastHitPosition(self, x, y):
        self.lastX = x
        self.lastY = y


    def StartButtonClick(self):
        #start gry, po zdefiniowaniu statków
        self.ids['player'].disabled = True
        self.ids['opponent'].disabled = False
        self.ids['StartButtonId'].disabled = True
        self.ids['gameId'].disabled = True
        print('Start Button Clik was click :)')
        self.isGameStarted = True
        self.sendMessage(PlayerConnectedMesage(self.ids['gameId'].text))

        # C:\Users\lunavis\Desktop\PyBattleShips2\battleships.py
        
    def onMessage(self, message: BaseMessage):
        # odbiera wiadomość
        if message.type == BaseMessage.ATTACK:
            x = message.x
            y = message.y
            self.ids['player'].ids[str(y)].ids[str(x)].setWasHit()

            if self.isShip(x, y) and self.isSunken(x, y, {}):
                self.sank(x, y, {}, 'player')
                self.sendMessage(SankMessage())
            elif self.isShip(x, y):
                self.sendMessage(HitMessage())
            else:
                self.sendMessage(MissMessage())
        elif message.type == BaseMessage.SANK:
            self.sank(self.lastX, self.lastY, {}, 'opponent')
        elif message.type == BaseMessage.HIT:
            self.ids['opponent'].ids[str(self.lastY)].ids[str(self.lastX)].hit()
        elif message.type == BaseMessage.MISS:
            self.ids['opponent'].ids[str(self.lastY)].ids[str(self.lastX)].miss()
        elif message.type == BaseMessage.GAME_ID_NOT_ALLOWED:
            self.ids['player'].disabled = False
            self.ids['opponent'].disabled = True
            self.ids['StartButtonId'].disabled = False
            self.ids['gameId'].disabled = False
            self.isGameStarted = False


    
    def sendMessage(self, message):
        # wysyła wiadomość
        if not self.isGameStarted:
            return
        # print(message)
        # self.onMessage(message)
        self.client.sendMessage(message)
        
    def isShip(self, x: int, y: int):
        # czy jest statkiem
        return self.ids['player'].ids[str(y)].ids[str(x)].isShip

    def wasHit(self, x: int, y: int):
        # czy jest trafiony
        return self.ids['player'].ids[str(y)].ids[str(x)].wasHit

    def isSunken(self, x, y, visited):
        if not self.isShip(x, y):
            return False

        if (x, y) not in visited:
            if self.wasHit(x, y):
                visited[(x, y)] = True

                for i in range(y-1, y+2):
                    if i == 0 or i == 11:
                        continue
                    for j in range(x-1, x+2):
                        if j == 0 or j == 11 or (i == y and j == x):
                            continue
                        if self.isShip(j, i) and not self.isSunken(j, i, visited):
                            return False
            else:
                return False

        return True

    def sank(self, x, y, visited, tag = "opponent"):
        if (x, y) not in visited:
            visited[(x, y)] = True
            for i in range(y - 1, y + 2):
                if i == 0 or i == 11:
                    continue
                for j in range(x - 1, x + 2):
                    if j == 0 or j == 11:
                        continue
                    self.ids[tag].ids[str(y)].ids[str(x)].setWasHit()
                    if self.ids[tag].ids[str(y)].ids[str(x)].isShip:
                        self.ids[tag].ids[str(y)].ids[str(x)].sank()
                        self.sank(j, i, visited, tag)


class BattleshipsApp(App):

    # def build(self):
    #     return Battleships()

    async def async_run(self, async_lib=None):
        self.load_config()
        self.load_kv(filename=self.kv_file)
        self.root = Battleships()
        await asyncio.gather(super(BattleshipsApp, self).async_run(async_lib=async_lib), self.root.client.run())

    def stop(self):
        self.root.client.stop()
        super(BattleshipsApp, self).stop()


