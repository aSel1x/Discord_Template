import asyncio

import discord
from loguru import logger
from dependency_injector.wiring import Provide, inject

from app import CustomBot
from app.core.config import Config
from app.core.ioc import AppProvider


@inject
async def main(
        config: Config = Provide[AppProvider.config],
):
    intents = discord.Intents.all()
    async with CustomBot(
            command_prefix=config.discord.prefix,
            intents=intents,
            config=config,
    ) as bot:
        await bot.start(config.discord.token)


if __name__ == '__main__':
    container = AppProvider()
    container.init_resources()
    container.wire(modules=[__name__])
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('bot stopped')
