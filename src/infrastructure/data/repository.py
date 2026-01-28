from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from infrastructure.db.account_model import AccountModel

class AccountRepository:
    """
    Repository for performing CRUD operations on AccountModel using an asynchronous SQLAlchemy session.

    This repository encapsulates all database access logic related to accounts,
    including creation, retrieval, update, deletion, and aggregation queries.

    Parameters
    ----------
    session : AsyncSession
        An asynchronous SQLAlchemy session used for database operations.

    Author Solonitsyn Maksym
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self) -> AccountModel:
        """
        Create a new account and persist it in the database.

        Returns
        -------
        AccountModel
            The created AccountModel instance with updated database fields.
        """
        account = AccountModel(number = 0, balance=0)
        self.session.add(account)
        await self.session.flush()

        account.number = account.id + 10000
        await self.session.flush()
        await self.session.refresh(account)
        return account

    async def get_account_by_number(self, number: int) -> AccountModel | None:
        """
        Retrieve an account by its unique number.

        Parameters
        ----------
        number : int
            The account number to search for.

        Returns
        -------
        AccountModel | None
            The AccountModel instance if found, otherwise None.
        """
        result = await self.session.execute(
            select(AccountModel).where(AccountModel.number == number)
        )
        return result.scalar_one_or_none()

    async def list_accounts(self) -> list[AccountModel]:
        """
        Retrieve all accounts from the database.

        Returns
        -------
        list[AccountModel]
            A list of all AccountModel instances.
        """
        result = await self.session.execute(select(AccountModel))
        return result.scalars().all()

    async def update_balance(self, number: int, new_balance: int) -> AccountModel | None:
        """
        Update the balance of an account.

        Parameters
        ----------
        number : int
            The account number to update.
        new_balance : int
            The new balance value.

        Returns
        -------
        AccountModel | None
            The updated AccountModel instance if found, otherwise None.
        """
        account = await self.get_account_by_number(number)
        if account is None:
            return None

        account.balance = new_balance
        await self.session.flush()
        await self.session.refresh(account)

        return account

    async def delete_account(self, number: int) -> bool:
        """
        Delete an account by its number.

        Parameters
        ----------
        number : int
            The account number to delete.

        Returns
        -------
        bool
            True if the account was found and deleted, False otherwise.
        """
        account = await self.get_account_by_number(number)
        if account is None:
            return False

        await self.session.delete(account)

        return True

    async def get_total_amount(self) -> int:
        """
        Calculate the total balance across all accounts.

        Returns
        -------
        int
            Sum of balances of all accounts. Returns 0 if no accounts exist.
        """
        result = await self.session.execute(select(func.sum(AccountModel.balance)))
        return result.scalar() or 0

    async def get_total_customer_count(self) -> int:
        """
        Count the total number of accounts.

        Returns
        -------
        int
            Number of accounts in the database. Returns 0 if no accounts exist.
        """
        result = await self.session.execute(select(func.count(AccountModel.id)))
        return result.scalar() or 0
