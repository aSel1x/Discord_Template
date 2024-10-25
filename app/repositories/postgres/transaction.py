from collections.abc import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker

from app import models

from .base import Repository


class TransactionRepo(Repository[models.Transaction]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=models.Transaction, session_maker=session_maker)

    async def retrieve_by_from_wallet(self, wallet_id: int) -> Sequence[models.Transaction]:
        return await self.retrieve_many(
            where_clauses=[self.model.from_wallet_id == wallet_id]
        )

    async def retrieve_by_to_wallet(self, wallet_id: int) -> Sequence[models.Transaction]:
        return await self.retrieve_many(
            where_clauses=[self.model.to_wallet == wallet_id]
        )

    async def retrieve_by_wallet(self, wallet_id: int) -> Sequence[models.Transaction]:
        return await self.retrieve_many(
            where_clauses=[
                self.model.to_wallet == wallet_id or self.model.from_wallet_id == wallet_id
            ]
        )
