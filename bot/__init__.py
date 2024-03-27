import traceback
import asyncio

from loguru import logger
from importlib import import_module
from sqlalchemy.ext.asyncio import AsyncSession
from discord import Interaction, app_commands
from discord.ext import commands

from . import cogs
from .core import settings, sign_all
from .database import Database


class CustomBot(commands.Bot):
    def __init__(
            self,
            *args,
            session: AsyncSession,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db = Database(session)

    async def setup_hook(self) -> None:
        for package in cogs.__all__:
            for cog in import_module("cogs." + package).__all__:
                logger.info(f"Loading extension: {package}:{cog}")
                await self.load_extension(name=f"cogs.{package}.{cog}")

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
        asyncio.create_task(sign_all(self), name="sign")
        logger.info(f"Logged in as: {self.user.name}, prefix: {self.command_prefix.__str__()}.")
