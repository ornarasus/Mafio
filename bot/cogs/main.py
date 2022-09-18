from discord.ext.commands import Bot

from bot.cogs.admin import register_admin_cogs
from bot.cogs.other import register_other_cogs
from bot.cogs.user import register_user_cogs
from bot.cogs.game import register_game_cogs


async def register_all_cogs(bot: Bot) -> None:
    cogs = (
        register_user_cogs,
        register_admin_cogs,
        register_other_cogs,
        register_game_cogs,
    )
    for cog in cogs:
        await cog(bot)
