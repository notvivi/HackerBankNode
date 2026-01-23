from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.db.base import Base

class AccountModel(Base):
     """
    Database entity representing a bank account.

    The Account entity encapsulates database rules related to
    account balance management and protects its invariants.
    Direct modification of the internal state is prohibited;
    all changes must be performed through domain.
    """

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
