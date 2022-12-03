
import asyncio


class Client:

    def __init__(self) -> None:
        self._stop = False

    async def run(self):
        while not self._stop:
            await asyncio.gather(self.send(), self.receive())

    async def send(self):
        print("Send")
        await asyncio.sleep(1)

    async def receive(self):
        print("Receive")
        await asyncio.sleep(1)

    def stop(self):
        self._stop = True