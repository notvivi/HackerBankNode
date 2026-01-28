import socket
import asyncio
import logging
from infrastructure.network.tcp_server import TCPServer
from infrastructure.logging.logging_config import setup_logging
from infrastructure.factories.command_factory import CommandFactory
from infrastructure.data.repository import AccountRepository
#from infrastructure.proxy.client import ProxyClient   # позже
from infrastructure.db.session import SessionManager
from infrastructure.network.tcp_handler import handle_client
from infrastructure.db.account_model import AccountModel
from infrastructure.db.session import engine

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(AccountModel.metadata.create_all)

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

async def main():
    setup_logging()

    local_ip = get_local_ip()
    print(local_ip)

    async with SessionManager() as session:
        factory = CommandFactory(local_ip=local_ip)


    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, factory),
        host="0.0.0.0",
        port=65530
    )

    addr = server.sockets[0].getsockname()
    logging.info(f"Bank node listening on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(init_db())
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'\nExiting...')
    except Exception:
        print('\nInternal Server Error\nExiting')
