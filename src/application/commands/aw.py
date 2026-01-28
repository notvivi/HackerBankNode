from application.commands.base import Command
from domain.bank.errors import DomainError
from domain.bank.account import Account

class WithdrawCommand(Command):
    def __init__(self, account: int, bank_ip: str, amount: int, local_ip: str, repo, proxy):
        self._account = account
        self._bank_ip = bank_ip
        self._amount = amount
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    async def execute(self) -> str:
        if self._bank_ip != self._local_ip:
            return await self._proxy.execute(
                self,
                self._bank_ip
            )

        accountModel = await self._repo.get_account_by_number(self._account)
        if not accountModel:
            raise DomainError("Account not found")

        account = Account(accountModel.number, accountModel.balance)

        try:
            account.withdraw(self._amount)
            await self._repo.update_balance(account.number, account.balance)
        except Exception as e:
            raise

        return "AW"
    def to_raw(self) -> str:
        return f"AW {self._account}/{self._bank_ip} {self._amount}"
