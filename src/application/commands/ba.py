from application.commands.base import Command
from domain.bank.account import Account
from domain.bank.errors import DomainError

class BankTotalAmmountCommand(Command):
    def __init__(self, bank_ip: str, local_ip: str, repo, proxy):
        self._bank_ip = bank_ip
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy
        self.result = 0

    async def execute(self) -> str:
        result = await self._repo.get_total_amount()
        self.result = result
        return f"BA {result}"
    def to_raw(self) -> str:
        return f"BA {self.result}"
