from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from .abc import AbstractRepository
from .. import models


class UserRepository(AbstractRepository[models.User]):
    type_model: type[models.User]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.User, session=session)

    async def new(
            self,
            discord_id: int,
            balance: Decimal | None = None
    ) -> models.User:
        model = models.User()
        model.discord_id = discord_id
        model.balance = balance

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_discord(self, discord_id: int) -> models.User | None:
        where_clauses = [self.type_model.discord_id == discord_id]
        entry = await self.get(where_clauses=where_clauses)
        return entry
