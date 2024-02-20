from pypresence import Presence
import time
import asyncio
from functools import partial

class DiscordRPC:
    def __init__(self, client_id):
        self.client_id = client_id
        self.rpc = None

    async def connect(self):
        await self._connect()

    async def _connect(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._init_rpc)

    def _init_rpc(self):
        self.rpc = Presence(self.client_id)
        self.rpc.connect()  # Appel bloquant exécuté de manière asynchrone

    async def update_rpc(self, artist, title, duration, link):
        if self.rpc is None:
            return

        start_time = time.time()
        # Utilisez partial pour pré-assigner des arguments à la fonction update
        func = partial(self.rpc.update, state=artist, details=title, end=start_time+duration, large_image="deezer", large_text="DeezcordRPC by @imluky", buttons=[{"label": "Listen on Deezer", "url": link}, {"label": "Get DeezcordRPC", "url": "https://github.com/lukyyy9/DeezcordRPC"}])
        await self._run_in_executor(func)

    async def clear_rpc(self):
        if self.rpc is None:
            return

        await self._run_in_executor(self.rpc.clear)

    def close(self):
        if self.rpc is not None:
            self.rpc.close()

    async def _run_in_executor(self, func, *args):
        loop = asyncio.get_running_loop()
        # Exécutez la fonction (avec ses arguments pré-assignés si utilisant partial) dans l'exécuteur
        await loop.run_in_executor(None, func, *args)
