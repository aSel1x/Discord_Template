
import discord as ds
from discord.ext import commands

from .base import BaseCog


class RatingCog(BaseCog):

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: ds.RawReactionActionEvent):
        match payload.emoji.name:
            case "👍":
                value = 1
            case "👎":
                value = -1
            case _:
                return
        user = await self.use_cases.user.retrieve_by_discord(payload.message_author_id)
        await self.use_cases.user.rating_change(user, value)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: ds.RawReactionActionEvent):
        match payload.emoji.name:
            case "👍":
                value = -1
            case "👎":
                value = 1
            case _:
                return
        partial_messageable = self.bot.get_partial_messageable(payload.channel_id, guild_id=payload.guild_id)
        message = await partial_messageable.fetch_message(payload.message_id)
        user = await self.use_cases.user.retrieve_by_discord(message.author.id)
        await self.use_cases.user.rating_change(user, value)

async def setup(bot):
    await bot.add_cog(RatingCog(bot))
