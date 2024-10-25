from typing import Literal

from discord import HTTPException, Object
from discord.ext import commands

from .base import BaseCog


class DeveloperCog(BaseCog):

    @commands.command(name='sync')
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
            self,
            ctx: commands.Context,
            guilds: commands.Greedy[Object],
            spec: Literal['~', '*', '^'] | None = None
    ) -> None:
        if not guilds:
            if spec == '~':
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == '*':
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == '^':
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

    async def __cogs_manage(
            self,
            ctx: commands.Context,
            action: Literal["load", "unload", "reload"],
            relative_path: str
    ) -> None:
        full_path = self.bot.extensions_path / relative_path
        if not full_path.exists():
            await ctx.send(f"Error: Cog file '{relative_path}' not found.")
            return

        module_path = (
                self.bot.extensions_path.as_posix().replace('/', '.') + '.'
                + relative_path.replace('/', '.').removesuffix('.py')
        )
        action_map = {
            "load": self.bot.load_extension,
            "unload": self.bot.unload_extension,
            "reload": self.bot.reload_extension
        }

        try:
            await action_map[action](module_path)
            await ctx.send(f"Cog '{relative_path}' {action}ed successfully.")
        except Exception as e:
            await ctx.send(f"Error {action}ing cog '{relative_path}': {str(e)}")

    @commands.command(name="cogs_manage")
    @commands.is_owner()
    async def cogs_manage(
            self, ctx: commands.Context, action: Literal['load', 'unload', 'reload'], relative_path: str
    ):
        await self.__cogs_manage(ctx, action, relative_path)

    @commands.command(name="cogs_list")
    @commands.is_owner()
    async def cogs_list(self, ctx: commands.Context):
        cogs = [
            str(p.relative_to(self.bot.extensions_path))
            for p in self.bot.extensions_path.rglob('*.py')
            if p.name not in ["__init__.py", "base.py"]
        ]
        if cogs:
            cogs_list = "\n".join(sorted(cogs))
            await ctx.send(f"Available cogs:\n```\n{cogs_list}\n```")
        else:
            await ctx.send("No cogs found.")


async def setup(bot):
    await bot.add_cog(DeveloperCog(bot))
