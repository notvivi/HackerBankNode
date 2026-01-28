from application.commands.base import Command
from domain.bank.errors import DomainError

class BalanceCommand(Command):
    def __init__(self, account: int, bank_ip: str, local_ip: str, repo, proxy):
        self._account = account
        self._bank_ip = bank_ip
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    async def execute(self) -> str:
        if self._bank_ip != self._local_ip:
            return await self._proxy.execute(
                self,
                self._bank_ip
            )

        acc = await self._repo.get_account_by_number(self._account)
        if not acc:
            raise DomainError("Account not found")

        return f"AB {acc.balance}"

    def to_raw(self) -> str:
        return f"AB {self._account}/{self._bank_ip}"
