

from kivy import Config

from battleships import BattleshipsApp


if __name__ == '__main__':
    Config.read('config.ini')
    BattleshipsApp().run()
