from decimal import Decimal

from sqlalchemy.types import BigInteger
from sqlmodel import Field, SQLModel

from .base import IDModel, TimestampModel


class UserBase(SQLModel):
    discord_id: int = Field(unique=True, sa_type=BigInteger)
    balance: Decimal = Field(default=Decimal(0.00), decimal_places=2)


class UserCreate(UserBase):
    pass


class User(UserBase, IDModel, TimestampModel, table=True):  # type: ignore
    pass
