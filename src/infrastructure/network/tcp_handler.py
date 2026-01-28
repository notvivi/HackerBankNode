import logging
from infrastructure.db.session import SessionManager
from infrastructure.data.repository import AccountRepository
from application.dtos.validation_error import ValidationError
from infrastructure.parsing.parser import parse


async def handle_client(reader, writer, factory):
    addr = writer.get_extra_info("peername")
    try:
        data = await reader.read(4096)
        if not data:
            return

        raw = data.decode().strip()
        logging.info(f"{addr} -> {raw}")

        try:
            parsed = parse(raw)

            async with SessionManager() as session:
                repo = AccountRepository(session)
                command = factory.create(parsed, repo, None)
                response = await command.execute()

        except ValidationError as ve:
            response = f"ER {ve}"
        except Exception as e:
            logging.exception(f"Command error: {e}")
            response = "ER Internal server error"

        logging.info(f"{addr} <- {response}")
        writer.write((response + "\n").encode())
        await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()
