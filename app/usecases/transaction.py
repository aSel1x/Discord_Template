from decimal import Decimal
from typing import TYPE_CHECKING

from app import models

if TYPE_CHECKING:
    from app.usecases import Services


class TransactionService:

    def __init__(self, service: 'Services'):
        self.service = service

    async def create(
            self,
            from_wallet: models.Wallet | None,
            to_wallet: models.Wallet,
            amount: Decimal | float,
    ):
        model = models.TransactionCreate(
            from_wallet_id=from_wallet.id if from_wallet else 0,
            to_wallet_id=to_wallet.id,
            amount=amount
        )
        await self.service.adapters.postgres.transaction.create(model)
