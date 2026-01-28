from application.commands.base import Command

class BankCodeCommand(Command):
    def __init__(self, local_ip: str):
        self._local_ip = local_ip

    async def execute(self) -> str:
        return f"BC {self._local_ip}"

    def to_raw(self) -> str:
        return f"BC {self._local_ip}"
