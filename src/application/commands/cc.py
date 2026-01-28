from application.commands.base import Command

class ConnectionCountCommand(Command):
    def __init__(self, connection_count: int):
        self.connection_count = connection_count

    async def execute(self) -> str:
        return f"CC {self.connection_count}"

    def to_raw(self) -> str:
       return f"CC {self.connection_count}"
