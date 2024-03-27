from typing import TYPE_CHECKING

from discord.ext.commands import Cog


if TYPE_CHECKING:
    from bot import CustomBot


class AbstractCog(Cog):
    def __init__(self, bot: 'CustomBot'):
        self.bot = bot
        self.db = bot.db
