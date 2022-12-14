from message import AttackMessage
from kivy.properties import BooleanProperty, DictProperty, ObjectProperty
from kivy.uix.button import Button

class GameButton(Button):
    coordinate = DictProperty({"x": 0, "y": 0})
    isShip = BooleanProperty(False)
    wasHit = BooleanProperty(False)
    isSunken = BooleanProperty(False)
    sendMessage = ObjectProperty()
    saveLastHitPosition = ObjectProperty()
    

    def on_release(self):
        super(GameButton, self).on_release()
        self.isShip = not self.isShip
        self.updateColor()
        self.sendMessage(AttackMessage(x=self.coordinate['x'], y=self.coordinate['y']))
        self.saveLastHitPosition(self.coordinate['x'], self.coordinate['y'])

    def setWasHit(self, value=True):
        self.wasHit = value
        self.updateColor()
        
    def hit(self):
        self.isShip = True
        self.setWasHit()
        print('Hit')
        
    def miss(self):
        self.isShip = False
        self.setWasHit()
        print('Miss')

    def sank(self):
        self.isSunken = True
        self.updateColor()

    def updateColor(self):
        if self.isSunken:
            self.background_color ="#a10514"
        elif self.isShip and self.wasHit:
            # self.background_color = (0.9, 0, 0)
            self.background_color = "#e0b01d"
        elif self.isShip and not self.wasHit:
            # self.background_color = (0, 0.9, 0)
            self.background_color = "#28a745"
        elif not self.isShip and self.wasHit:
            # self.background_color = (0, 0, 0.9)
            self.background_color = "#007bff"
        elif not self.isShip and not self.wasHit:
            self.background_color = (0.3, 0.3, 0.3)

