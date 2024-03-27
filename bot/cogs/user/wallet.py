import discord as ds
from discord import app_commands

from ..abc import AbcCog


class UserWalletCog(AbcCog):

    @app_commands.command(name='transfer', description='Transfer some coins to another user')
    @app_commands.describe(receiver='Who will receive transfer')
    @app_commands.describe(amount='How much coins')
    async def coin_transfer(
            self,
            interaction: ds.Interaction,
            receiver: ds.User | ds.Member,
            amount: int
    ) -> ds.InteractionMessage:
        if not (sender := await self.db.user.retrieve_by_discord(interaction.user.id)):
            return await interaction.response.send_message(content='Unexpected error.')

        if sender.balance - amount < 0:
            return await interaction.response.send_message(content='Needs to raise coins')

        if not (receiver := await self.db.user.retrieve_by_discord(receiver.id)):
            return await interaction.response.send_message(content='Unexpected error.')

        sender.balance -= amount
        receiver.balance += amount
        await self.db.session.commit()

        return await interaction.response.send_message(content='Success')


async def setup(bot):
    await bot.add_cog(UserWalletCog(bot))
