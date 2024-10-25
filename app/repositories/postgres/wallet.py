from sqlalchemy.ext.asyncio import async_sessionmaker

from app import models

from .base import Repository


class WalletRepo(Repository[models.Wallet]):
    def __init__(self, session_maker: async_sessionmaker):
        super().__init__(model=models.Wallet, session_maker=session_maker)

    async def retrieve_by_user(self, user_id: int) -> models.Wallet | None:
        return await self.retrieve_one(
            where_clauses=[self.model.user_id == user_id]
        )
