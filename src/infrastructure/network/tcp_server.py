import asyncio
import logging
from infrastructure.network.tcp_handler import handle_client

class TCPServer:
    def __init__(self, host: str, port: int, factory):
        self.host = host
        self.port = port
        self.factory = factory
        self.server = None

    async def start(self):
        self.server = await asyncio.start_server(
            lambda r, w: handle_client(r, w, self.factory),
            self.host, self.port
        )
        addr = self.server.sockets[0].getsockname()
        logging.info(f"Bank node listening on {addr}")

        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()
