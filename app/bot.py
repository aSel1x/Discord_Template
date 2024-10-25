import traceback
from pathlib import Path

from loguru import logger
from discord import Interaction, app_commands
from discord.ext import commands
from sqlalchemy import exc as sa_exc

from app import models
from app.core.config import Config
from app.core.ioc import AppProvider
from app.controllers import bot


class CustomBot(commands.Bot):
    def __init__(
            self,
            *args,
            config: Config,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.config = config
        self.extensions_path = Path("app", "controllers", "bot")
        self.container = AppProvider()

    async def __sign_all(self) -> None:
        use_cases = await self.container.use_cases()
        for guild in self.guilds:
            for member in guild.members:
                try:
                    await use_cases.user.create(
                        models.UserCreate(discord_id=member.id)
                    )
                except sa_exc.IntegrityError:
                    pass


    async def setup_hook(self) -> None:
        extension_path = str(self.extensions_path).replace('/', '.')
        for cog in bot.__all__:
            await self.load_extension(extension_path + '.' + cog)
            logger.info(f"{cog=} loaded")


    async def on_command_error(self, ctx: commands.Context, error) -> None:
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"{error}")
        else:
            logger.info(f"Ignoring exception in command {ctx.command}:")
            traceback.print_exception(type(error), error, error.__traceback__)

    async def on_app_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.CommandOnCooldown):
            await interaction.response.send_message(f"{error}")
        else:
            logger.info(f"Ignoring exception in command {interaction.command}:")
            traceback.print_exception(type(error), error, error.__traceback__)

    async def on_ready(self) -> None:
        logger.info(f"Logged in as: {self.user.name}, prefix: {self.command_prefix.__str__()}.")
        await self.__sign_all()
