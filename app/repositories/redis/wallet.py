from redis.asyncio import Redis

from app import models

from .base import Repository


class WalletRepo(Repository[models.Wallet]):
    def __init__(self, client: Redis):
        super().__init__(model=models.Wallet, client=client)
