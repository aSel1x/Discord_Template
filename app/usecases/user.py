from typing import TYPE_CHECKING

from app import models
from app.core import exception

if TYPE_CHECKING:
    from app.usecases import Services


class UserService:
    def __init__(self, service: "Services"):
        self.service = service

    @staticmethod
    def __buffer_ds_to_sys_key(discord_id) -> str:
        return f"ds-to-sys:{discord_id}"

    async def create(self, user: models.UserCreate) -> models.User:
        user = await self.service.adapters.postgres.user.create(user)
        await self.service.wallet.create(models.WalletCreate(user_id=user.id))
        return user

    async def retrieve_by_discord(self, discord_id: int) -> models.User:
        buffer_key = self.__buffer_ds_to_sys_key(discord_id)
        if sys_id := await self.service.aiobuffer.get(buffer_key):
            if user := await self.service.adapters.redis.user.retrieve_one(sys_id):
                return user
            if user := await self.service.adapters.postgres.user.retrieve_one(sys_id):
                return user
        if user := await self.service.adapters.postgres.user.retrieve_by_discord(discord_id):
            await self.service.aiobuffer.set(buffer_key, user.id)
            return user

        raise exception.user.NotFound

    async def rating_change(self, user: models.User, value: int) -> None:
        user.rating += value
        await self.service.adapters.redis.user.create(user)
        await self.service.adapters.postgres.user.update(user.id, user.model_dump(include={'rating'}))
