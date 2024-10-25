from typing import TYPE_CHECKING

from sqlalchemy.types import BigInteger
from sqlmodel import Field, SQLModel, Relationship

from .base import IDModel, TimestampModel

if TYPE_CHECKING:
    from .wallet import Wallet


class UserBase(SQLModel):
    discord_id: int = Field(unique=True, sa_type=BigInteger)


class UserCreate(UserBase):
    pass


class User(UserBase, IDModel, TimestampModel, table=True):  # type: ignore
    rating: int = 0
    wallet: "Wallet" = Relationship(back_populates="user")
