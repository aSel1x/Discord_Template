from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    discord_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True, nullable=False)
    balance: Mapped[Decimal] = mapped_column(sa.DECIMAL(scale=2), unique=False, default=Decimal(0.00))

    def __repr__(self):
        return f"{__class__.__name__}({self.id=}, {self.balance=})"
