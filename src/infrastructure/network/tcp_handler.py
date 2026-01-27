import logging
from infrastructure.parsing.parser import parse
from application.dtos.validation_error import ValidationError



async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, factory):
    addr = writer.get_extra_info("peername")
    try:
        data = await reader.read(4096)
        if not data:
            return

        raw = data.decode().strip()
        logging.info(f"{addr} -> {raw}")

        try:
            parsed = parse(raw)
            command = factory.create(parsed)
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
