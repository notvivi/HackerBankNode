import random
from sqlite3 import IntegrityError

from application.commands.base import Command
from domain.bank.account import Account
from domain.bank.errors import DomainError

class CreateAccountCommand(Command):
    def __init__(self, local_ip: str, repo, proxy):
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    async def execute(self) -> str:
        for _ in range(5):  # avoid infinite loop
            acc = Account(random.randint(10000, 99999), 0)
            try:
                await self._repo.add(acc.number, acc.balance)
                return f"AC {acc.number}/{self._local_ip}"
            except IntegrityError:
                await self._repo.session.rollback()

        raise DomainError("Unable to generate unique account number")