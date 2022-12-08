

import asyncio
from kivy import Config

from battleships import BattleshipsApp


if __name__ == '__main__':
    Config.read('config.ini')
    # BattleshipsApp().run()
    # print("somthing wrong")


    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        BattleshipsApp().async_run(async_lib='asyncio')
    )
    

