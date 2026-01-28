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
        try:
            print(1)
            acc = await self._repo.add()
            print(2)
            return f"AC {acc.number}/{self._local_ip}"
        except Exception:
            await self._repo.session.rollback()
