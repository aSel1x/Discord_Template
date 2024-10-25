from typing import TYPE_CHECKING

from discord.ext.commands import Cog

from app.usecases import Services

if TYPE_CHECKING:
    from app import CustomBot


class BaseCog(Cog):
    use_cases: Services
    def __init__(self, bot: 'CustomBot'):
        self.bot = bot

    async def cog_load(self) -> None:
        self.use_cases = await self.bot.container.use_cases()
