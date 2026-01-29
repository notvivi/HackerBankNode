import os
import socket
import asyncio
import logging
import sys

print("\n" + "="*40)
print("INICIALIZACE APLIKACE")
is_frozen = getattr(sys, 'frozen', False)
print(f"Běží jako EXE: {is_frozen}")

if is_frozen:
    # Cesta, kde je rozbalený obsah (včetně _internal)
    base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    print(f"Base Directory: {base}")
    # Přesná cesta k tvému configu
    target = os.path.join(base, "_internal", "src", "config.json")
    print(f"Pokus o nalezení configu: {target}")
    print(f"Existuje soubor? {'ANO' if os.path.exists(target) else 'NE'}")
else:
    print(f"Vývojové prostředí, hledám v: {os.path.abspath('src/config.json')}")
print("="*40 + "\n")

from infrastructure.config.config import load_config
from infrastructure.network.tcp_handler import handle_client
from infrastructure.logging.logging_config import setup_logging
from infrastructure.factories.command_factory import CommandFactory
from infrastructure.db.session import SessionManager, engine
from infrastructure.db.account_model import AccountModel
from infrastructure.proxy.bank_proxy import BankProxy

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(base_path, "..", "lib"))
sys.path.insert(0, os.path.join(base_path, "lib"))

import resource_path


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(AccountModel.metadata.create_all)


def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


def get_config_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    dist_path = os.path.join(current_dir, "ui", "dist", "app", "_internal", "src", "config.json")

    dev_path = os.path.join(current_dir, "config.json")

    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base_dir, "_internal", "src", "config.json")

    if os.path.exists(dist_path):
        return dist_path

    if os.path.exists(dev_path):
        return dev_path


    return dev_path

CONFIG_PATH = get_config_path()
config = load_config(CONFIG_PATH)

async def main():
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

