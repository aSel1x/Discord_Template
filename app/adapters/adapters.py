from contextlib import AsyncExitStack, asynccontextmanager
from typing import AsyncIterator

from app.core.config import Config

from .postgres import PostgresDB
from .redis import RedisDB


class Adapters:
    def __init__(
            self,
            postgres: PostgresDB,
            redis: RedisDB,
    ) -> None:
        self.postgres = postgres
        self.redis = redis

    @classmethod
    @asynccontextmanager
    async def create(cls, config: Config) -> AsyncIterator['Adapters']:
        async with AsyncExitStack() as stack:
            postgres = await stack.enter_async_context(PostgresDB(config.postgres.dsn))
            redis = await stack.enter_async_context(RedisDB(config.redis.dsn))

            yield cls(postgres, redis)
