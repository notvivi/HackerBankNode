from domain.errors import DomainError

class Account:
    """
    Domain entity representing a bank account.

    The Account entity encapsulates business rules related to
    account balance management and protects its invariants.
    Direct modification of the internal state is prohibited;
    all changes must be performed through domain methods.

    Invariants
    ----------
    - Account number must be in range [10000, 99999]
    - Balance must never be negative

    Attributes
    ----------
    number : int
        Unique account identifier in range 10000–99999.
        Read-only property.
    balance : int
        Current account balance in dollars.
        Read-only property.
    """

    def __init__(self, number: int, balance: int):
        """
        Create a new Account entity.

        Parameters
        ----------
        number : int
            Unique account identifier in range 10000–99999.
        balance : int
            Initial account balance. Must be non-negative.

        Raises
        ------
        DomainError
            If the account number is out of range or
            the initial balance is negative.
        """
        self._validate_number(number)
        self._validate_balance(balance)

        self._number = number
        self._balance = balance

    @property
    def number(self) -> int:
        """
        Get the account number.

        Returns
        -------
        int
            Account number in range 10000–99999.
        """
        return self._number

    @property
    def balance(self) -> int:
        """
        Get the current account balance.

        Returns
        -------
        int
            Current balance in dollars.
        """
        return self._balance

    def withdraw(self, amount: int) -> None:
        """
        Withdraw funds from the account.

        Parameters
        ----------
        amount : int
            Amount to withdraw. Must be positive and
            not exceed the current balance.

        Raises
        ------
        DomainError
            If the amount is not positive or
            if there are insufficient funds.
        """
        if amount <= 0:
            raise DomainError("Withdraw amount must be positive")

        if amount > self._balance:
            raise DomainError("Insufficient funds")

        self._balance -= amount

    def deposit(self, amount: int) -> None:
        """
        Deposit funds into the account.

        Parameters
        ----------
        amount : int
            Amount to deposit. Must be positive.

        Raises
        ------
        DomainError
            If the deposit amount is not positive.
        """
        if amount <= 0:
            raise DomainError("Deposit amount must be positive")

        self._balance += amount

    @staticmethod
    def _validate_number(number: int) -> None:
        """
        Validate account number.

        Parameters
        ----------
        number : int
            Account number to validate.

        Raises
        ------
        DomainError
            If the account number is out of range.
        """
        if not 10000 <= number <= 99999:
            raise DomainError("Invalid account number")

    @staticmethod
    def _validate_balance(balance: int) -> None:
        """
        Validate account balance.

        Parameters
        ----------
        balance : int
            Balance value to validate.

        Raises
        ------
        DomainError
            If the balance is negative.
        """
        if balance < 0:
            raise DomainError("Balance cannot be negative")

