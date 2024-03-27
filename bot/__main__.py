import asyncio
import discord

from loguru import logger

from bot import CustomBot
from bot.core import settings
from bot.database import new_session


async def main():
    discord.utils.setup_logging()
    intents = discord.Intents.all()
    logger.add("bot.log", level=0, colorize=False, backtrace=True, diagnose=True)
    async with await new_session() as session:
        async with CustomBot(
            command_prefix=settings.DISCORD_BOT_PREFIX,
            session=session,
            intents=intents,
        ) as bot:
            await bot.start(settings.DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("bot stopped")
