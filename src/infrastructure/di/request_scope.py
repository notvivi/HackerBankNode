from infrastructure.db.session import AsyncSessionLocal
from infrastructure.data.account_repository import AccountRepository
from application.services.bank_service import BankService

class RequestScope:
    """Scoped objects for a single request."""

    def __init__(self):
        self.session = None
        self.repo = None
        self.service = None

    async def __aenter__(self):
        self.session = AsyncSessionLocal()
        self.repo = AccountRepository(self.session)
        self.service = BankService(self.repo)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
