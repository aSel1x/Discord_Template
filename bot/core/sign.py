from typing import TYPE_CHECKING

from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from bot import CustomBot


async def sign_all(bot: 'CustomBot'):
    for guild in bot.guilds:
        for member in guild.members:
            try:
                await bot.db.user.new(
                    discord_id=member.id
                )
            except IntegrityError:
                await bot.db.session.rollback()
    await bot.db.session.commit()
