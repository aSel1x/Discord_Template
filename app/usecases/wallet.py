from typing import TYPE_CHECKING
from decimal import Decimal

from app import models
from app.core import exception

if TYPE_CHECKING:
    from app.usecases import Services


class WalletService:

    def __init__(self, service: 'Services'):
        self.service = service

    @staticmethod
    def __buffer_user_to_wallet_key(user_id: int) -> str:
        return f"user_to_wallet_key:{user_id}"

    async def create(self, wallet: models.WalletCreate) -> models.Wallet:
        wallet = await self.service.adapters.postgres.wallet.create(wallet)
        await self.service.adapters.redis.wallet.create(wallet)
        return wallet

    async def retrieve_by_user(self, user_id: int) -> models.Wallet:
        buffer_key = self.__buffer_user_to_wallet_key(user_id)
        if wallet_id := await self.service.aiobuffer.get(buffer_key):
            if wallet := await self.service.adapters.redis.wallet.retrieve_one(wallet_id):
                return wallet
            if wallet := await self.service.adapters.postgres.wallet.retrieve_one(wallet_id):
                return wallet
        if wallet := await self.service.adapters.postgres.wallet.retrieve_by_user(user_id):
            await self.service.aiobuffer.set(buffer_key, wallet.id)
            return wallet

    async def transaction(
            self,
            from_wallet: models.Wallet | None,
            to_user: models.User,
            amount: int | float,
    ) -> None:

        amount = Decimal(amount)

        if from_wallet is not None:
            if from_wallet.balance - amount < 0:
                raise exception.transaction.NotEnoughBalance

        to_wallet = await self.retrieve_by_user(to_user.id)

        to_wallet.balance += amount

        await self.service.adapters.postgres.wallet.update(
            to_wallet.id, to_wallet.model_dump(include={'balance'})
        )

        await self.service.transaction.create(from_wallet, to_wallet, amount)
