from domain.bank.account import Account
from application.dtos.create_account_dto import CreateAccountDto
from domain.bank.errors import DomainError


class BankService:
    """
    Application service for bank operations.

    Responsibilities:
    - Decide whether to handle request locally or proxy it
    - Coordinate domain objects
    - Persist data via repository
    """

    def __init__(
        self,
        repository,
        proxy,
        own_bank_address: str,
    ):
        self._repo = repository
        self._proxy = proxy
        self._own_address = own_bank_address

    async def create_account(self, dto: CreateAccountDto) -> str:
        """
        Create a bank account.

        If the target bank address is not local,
        the request is proxied to another node.
        """

        if dto.bank_address != self._own_address:
            return await self._proxy.forward_create_account(dto)

        try:
            account = Account(
                number=dto.number,
                balance=dto.balance,
            )
        except DomainError:
            raise

        await self._repo.add(account)

        return f"AC {account.number}/{self._own_address}"

    async def
