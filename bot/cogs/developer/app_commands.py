from typing import TYPE_CHECKING, Literal, Optional

from discord import Object, HTTPException
from discord.ext import commands

from bot.cogs.abc import AbstractCog

if TYPE_CHECKING:
    from bot import CustomBot


class DeveloperAppCmdCog(AbstractCog, name="DeveloperAppCommandsCog"):

    def __init__(self, bot: 'CustomBot'):
        super().__init__(bot)

    @commands.command(name="sync")
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self,
                   ctx: commands.Context,
                   guilds: commands.Greedy[Object],
                   spec: Optional[Literal["~", "*", "^"]] = None
                   ) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    await bot.add_cog(DeveloperAppCmdCog(bot))
