from dependency_injector import containers, providers

from .config import Config
from app.adapters import Adapters
from app.usecases import Services


async def get_adapters(config: Config) -> Adapters:
    async with Adapters.create(config) as adapters:
        return adapters


class AppProvider(containers.DeclarativeContainer):
    config = providers.Factory(Config)

    adapters = providers.Coroutine(get_adapters, config=config)
    use_cases = providers.Factory(Services, adapters=adapters, config=config)
