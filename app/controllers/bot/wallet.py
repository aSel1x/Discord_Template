from logging import exception

import discord as ds
from discord import app_commands

from .base import BaseCog
from app.core import exception


class WalletCog(BaseCog):

    @app_commands.command(
        name="transaction", description="Transfer some coins to any user"
    )
    @app_commands.describe(receiver="Who will receive transfer")
    @app_commands.describe(amount="How much coins")
    async def transaction(
            self,
            interaction: ds.Interaction,
            receiver: ds.User | ds.Member,
            amount: int,
    ) -> ds.InteractionMessage:

        sender = await self.use_cases.user.retrieve_by_discord(interaction.user.id)
        from_wallet = await self.use_cases.wallet.retrieve_by_user(sender.id)

        if not (receiver := await self.use_cases.user.retrieve_by_discord(receiver.id)):
            return await interaction.response.send_message(
                content="Receiver not founded."
            )

        try:
            await self.use_cases.wallet.transaction(from_wallet, receiver, amount)
        except exception.transaction.NotEnoughBalance:
            return await interaction.response.send_message("Not enough money.")

        return await interaction.response.send_message(content="Success")


async def setup(bot):
    await bot.add_cog(WalletCog(bot))
