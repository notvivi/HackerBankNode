import logging
import asyncio
from infrastructure.db.session import SessionManager
from infrastructure.data.repository import AccountRepository
from application.dtos.validation_error import ValidationError
from infrastructure.parsing.parser import parse
from application.commands.cc import ConnectionCountCommand
from domain.bank.errors import DomainError
connection_count = 0
connection_lock = asyncio.Lock()

WELCOME_MESSAGE = """\
===============================================================
------------------------- HACKER BANK -------------------------
===============================================================
Command List:
---------------------------------------------------------------
Name                     Command
---------------------------------------------------------------
Bank code                 BC
Account create            AC
Account deposit           AD <account>/<bank_ip> <amount>
Account withdrawal        AW <account>/<bank_ip> <amount>
Account balance           AB <account>/<bank_ip>
Account remove            AR <account>/<bank_ip>
Bank total amount         BA <bank_ip>
Bank number of clients    BN <bank_ip>
---------------------------------------------------------------
"""

def format_for_terminal(msg: str) -> str:
    return msg.replace("\n", "\r\n")

async def add_connection():
    global connection_count
    async with connection_lock:
        connection_count += 1
        return connection_count


async def remove_connection():
    global connection_count
    async with connection_lock:
        connection_count -= 1
        return connection_count


async def handle_client(reader, writer, factory):
    addr = writer.get_extra_info("peername")
    await add_connection()
    response = "ER Internal server error"

    try:
        writer.write(format_for_terminal(WELCOME_MESSAGE + "\r\n").encode())
        await writer.drain()

        while True:
            data = await reader.read(4096)
            if not data:
                break

            raw = data.decode().strip()
            logging.info(f"{addr} -> {raw}")

            try:
                parsed = parse(raw)

                async with SessionManager() as session:
                    repo = AccountRepository(session)
                    command = factory.create(parsed, repo, None)

                    if isinstance(command, ConnectionCountCommand):
                        command.connection_count = connection_count

                    response = await command.execute()

            except ValidationError as ve:
                response = f"ER {ve}"
            except DomainError as de:
                response = f"ER {de}"
            except Exception as e:
                logging.exception(f"Command error: {e}")
                response = "ER Internal server error"

            logging.info(f"{addr} <- {response}")
            writer.write(format_for_terminal(response + "\r\n").encode())
            await writer.drain()

    finally:
        await remove_connection()
        writer.close()
        await writer.wait_closed()
