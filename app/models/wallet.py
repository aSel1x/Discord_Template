from typing import TYPE_CHECKING
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

from .base import IDModel, TimestampModel

if TYPE_CHECKING:
    from .user import User
    from .transaction import Transaction


class WalletBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")


class WalletCreate(WalletBase):
    pass


class Wallet(WalletBase, IDModel, TimestampModel, table=True):  # type: ignore
    balance: Decimal = Field(default=Decimal('0.00'), decimal_places=2)

    user: "User" = Relationship(back_populates="wallet")
    transactions_from: list["Transaction"] = Relationship(
        back_populates="from_wallet",
        sa_relationship_kwargs={"foreign_keys": "Transaction.from_wallet_id"}
    )
    transactions_to: list["Transaction"] = Relationship(
        back_populates="to_wallet",
        sa_relationship_kwargs={"foreign_keys": "Transaction.to_wallet_id"}
    )
