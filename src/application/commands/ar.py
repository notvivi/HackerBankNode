from application.commands.base import Command
from domain.bank.account import Account
from domain.bank.errors import DomainError

class RemoveAccountCommand(Command):
    def __init__(self, account_number: int, bank_ip: str, local_ip: str, repo, proxy):
        self._account_number = account_number
        self._bank_ip = bank_ip
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    async def execute(self) -> str:
        if self._bank_ip != self._local_ip:
            return await self._proxy.forward(f"AR {self._account_number}/{self._bank_ip}")

        account = await self._repo.get_account_by_number(self._account_number)

        if not account:
            raise DomainError("Account does not exists")

        await self._repo.delete_account(account.number)

        return f"AR"

