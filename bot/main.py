import asyncio

from discord import Intents
from discord.ext.commands import Bot

from bot.misc import Env, Config
from bot.cogs import register_all_cogs
from bot.database.models import register_models


def start_bot():
    intents = Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.reactions = True
    intents.members = True

    bot = Bot(Config.CMD_PREFIX, intents=intents)
    asyncio.run(register_all_cogs(bot))
    register_models()

    bot.run(Env.TOKEN)
