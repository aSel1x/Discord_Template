from app.adapters import Adapters
from app.core.config import Config
from app.utils.buffer import AsyncBuffer

from .user import UserService
from .wallet import WalletService
from .transaction import TransactionService


class Services:
    def __init__(self, adapters: Adapters, config: Config):
        self.config = config
        self.adapters = adapters

        self.aiobuffer = AsyncBuffer()

        self.user = UserService(self)
        self.wallet = WalletService(self)
        self.transaction = TransactionService(self)
