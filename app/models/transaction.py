from typing import TYPE_CHECKING
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

from .base import IDModel, TimestampModel

if TYPE_CHECKING:
    from .wallet import Wallet


class TransactionBase(SQLModel):
    from_wallet_id: int = Field(foreign_key="wallet.id")
    to_wallet_id: int = Field(foreign_key="wallet.id")
    amount: Decimal = Field(decimal_places=2)


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase, IDModel, TimestampModel, table=True):  # type: ignore

    from_wallet: "Wallet" = Relationship(
        back_populates="transactions_from",
        sa_relationship_kwargs={"foreign_keys": "Transaction.from_wallet_id"}
    )
    to_wallet: "Wallet" = Relationship(
        back_populates="transactions_to",
        sa_relationship_kwargs={"foreign_keys": "Transaction.to_wallet_id"}
    )