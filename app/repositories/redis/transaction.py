from redis.asyncio import Redis

from app import models

from .base import Repository


class TransactionRepo(Repository[models.Transaction]):
    def __init__(self, client: Redis):
        super().__init__(model=models.Transaction, client=client)
