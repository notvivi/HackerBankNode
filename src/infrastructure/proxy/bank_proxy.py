import asyncio
import logging


class BankProxy:
    """
    Proxy for forwarding commands to other bank nodes by IP.
    """

    def __init__(self, local_ip: str, port: int, timeout: int):
        self.local_ip = local_ip
        self.port = port
        self.timeout = timeout

    async def execute(self, command, bank_ip: str):
        if bank_ip is None or bank_ip == self.local_ip:
            return await command.execute()

        return await self._forward_to_remote(command, bank_ip)

    async def _forward_to_remote(self, command, bank_ip: str):
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(bank_ip, self.port),
                timeout=self.timeout
            )

            raw = command.to_raw()
            writer.write((raw + "\n").encode())
            await writer.drain()

            data = await reader.read(4096)
            response = data.decode().strip()

            writer.close()
            await writer.wait_closed()
            return response

        except asyncio.TimeoutError:
            return "ER Remote bank timeout"
        except Exception as e:
            logging.exception(f"Proxy error forwarding to {bank_ip}: {e}")
            return "ER Could not forward command"

    async def is_bank(self, ip, port, timeout) -> bool:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout
            )
            writer.write(b"BC\n")
            await writer.drain()

            data = await asyncio.wait_for(reader.read(64), timeout)
            writer.close()
            await writer.wait_closed()

            return data.startswith(b"BC")
        except Exception:
            return False

    async def raw(self, ip, port, cmd: str) -> str:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.write(f"{cmd}\n".encode())
        await writer.drain()

        data = await reader.read(128)
        writer.close()
        await writer.wait_closed()

        return data.decode().strip()
