import socket
import asyncio
import logging

from infrastructure.config.config import load_config
from infrastructure.network.tcp_handler import handle_client
from infrastructure.logging.logging_config import setup_logging
from infrastructure.factories.command_factory import CommandFactory
from infrastructure.db.session import SessionManager, engine
from infrastructure.db.account_model import AccountModel
from infrastructure.proxy.bank_proxy import BankProxy


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(AccountModel.metadata.create_all)


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


async def main():
    config = load_config("src/config.json")

    setup_logging(config.log_file)

    local_ip = get_local_ip()
    logging.info(f"Local IP: {local_ip}")

    proxy = BankProxy(
        local_ip=local_ip,
        port=config.port,
        timeout=config.timeout,
    )

    factory = CommandFactory(
        local_ip=local_ip,
        config = config
    )

    await init_db()

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, factory, proxy),
        host=local_ip,
        port=config.port
    )

    addr = server.sockets[0].getsockname()
    logging.info(f"Bank node listening on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logging.exception(e)
        print("\nInternal Server Error\nExiting")

