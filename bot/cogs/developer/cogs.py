import os
from typing import TYPE_CHECKING

from discord.ext import commands, tasks

from ..abc import AbstractCog

if TYPE_CHECKING:
    from bot import CustomBot


class DeveloperCogsCog(AbstractCog, name="DeveloperCogsCog"):

    def __init__(self, bot: 'CustomBot'):
        super().__init__(bot)

    @commands.command(name="reload")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, folder: str) -> None:
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            await self.bot.reload_extension(f"cogs.{folder}.cog")
            await ctx.send(f"{folder} cog reloaded")

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, folder: str) -> None:
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            await self.bot.unload_extension(f"cogs.{folder}.cog")
            await ctx.send(f"{folder} cog unloaded")

    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx: commands.Context, folder: str) -> None:
        if os.path.exists(os.path.join("cogs", folder, "cog.py")):
            await self.bot.load_extension(f"cogs.{folder}.cog")
            await ctx.send(f"{folder} cog loaded")


async def setup(bot):
    await bot.add_cog(DeveloperCogsCog(bot))
