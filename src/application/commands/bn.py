from application.commands.base import Command
from domain.bank.account import Account
from domain.bank.errors import DomainError

class BankNumberClientCommand(Command):
    def __init__(self, bank_ip: str, local_ip: str, repo, proxy):
        self._bank_ip = bank_ip
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    async def execute(self) -> str:
        result = await self._repo.get_total_customer_count()

        return f"BN {result}"
