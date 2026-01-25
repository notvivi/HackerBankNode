import pytest
from src.domain.bank.account import Account
from src.domain.bank.errors import DomainError

def test_account_creation():
    acc = Account(number=12345, balance=100)
    assert acc.number == 12345
    assert acc.balance == 100

def test_account_negative_balance_raises():
    with pytest.raises(DomainError):
        Account(number=12345, balance=-10)

def test_account_invalid_number_raises():
    with pytest.raises(DomainError):
        Account(number=999, balance=0)

def test_deposit_withdraw():
    acc = Account(number=12345, balance=100)
    acc.deposit(50)
    assert acc.balance == 150
    acc.withdraw(70)
    assert acc.balance == 80

    with pytest.raises(DomainError):
        acc.withdraw(1000)
    with pytest.raises(DomainError):
        acc.deposit(-5)
