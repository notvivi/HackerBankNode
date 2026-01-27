from application.dtos.validation_error import ValidationError

class CreateAccountDto:
    """
    Data transfer object for account creation.

    Invariants
    ----------
    - Account number must be in range [10000, 99999]
    - Balance must never be negative
    - BankAdress is an ip adress
    Attributes
    ----------
    bank_address : str
        Ipv4 adress
    number : int
        Unique account identifier in range 10000–99999.
        Read-only property.
    balance : int
        Current account balance in dollars.
        Read-only property.

    Author : Solonitsyn Maksym
    """
    def __init__(self, bank_address, number):
        self._validate_number(number)
        self._validate_bank_address(bank_address)

        self._bank_adress = bank_address
        self._number = number

    def bank_address(self) -> str:
        """
        Get the bank addresS

        Returns
        -------
        str
            Bank ip address
        """
        return self._bank_adress

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
        ValidationError
            If the account number is out of range.
        """
        if not 10000 <= number <= 99999:
            raise ValidationError("Invalid account number")

    @staticmethod
    def _validate_bank_address(address: str) -> None:
        """
        Validate bank ip adress

        Parameters
        ----------
        adress : str
            Ipv4 adress

        Raises
        ---------
        ValidationError
            If the adress is not valid
        """
        try:
            ipaddress.ip_address(address)
        except ValueError:
            raise ValidationError("Invalid bank IP address")
