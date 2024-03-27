from typing import TYPE_CHECKING

import discord as ds
from discord import app_commands

from ..abc import AbstractCog

if TYPE_CHECKING:
    from bot import CustomBot


class UserWalletCog(AbstractCog, name="UserWalletCog"):

    def __init__(self, bot: 'CustomBot'):
        super().__init__(bot)

    @app_commands.command(name="transfer", description="Transfer some coins to another user")
    @app_commands.describe(receiver="Who will receive transfer")
    @app_commands.describe(amount="How much coins")
    async def coin_transfer(
            self,
            interaction: ds.Interaction,
            receiver: ds.User | ds.Member,
            amount: int
    ) -> ds.InteractionMessage:
        sender = await self.db.user.get_by_discord(interaction.user.id)

        if sender.balance - amount < 0:
            return await interaction.response.send_message(content="Needs to raise coins")

        sender.balance -= amount
        receiver = await self.db.user.get_by_discord(receiver.id)
        receiver.balance += amount
        await self.db.session.commit()

        return await interaction.response.send_message(content="Success")


async def setup(bot):
    await bot.add_cog(UserWalletCog(bot))
