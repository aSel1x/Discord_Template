import asyncio

import discord
from loguru import logger

from bot import CustomBot
from bot.core import settings
from bot.core.db import SessionLocal


async def main():
    intents = discord.Intents.all()
    logger.add('bot.log', level=0, colorize=False, backtrace=True, diagnose=True)
    async with SessionLocal() as session:
        async with CustomBot(
            command_prefix=settings.DISCORD_BOT_PREFIX,
            session=session,
            intents=intents,
        ) as bot:
            await bot.start(settings.DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('bot stopped')
