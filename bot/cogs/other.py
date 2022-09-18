import os

import discord
from discord.ext.commands import Bot, Cog

from bot.api.server import Server
from bot.managers.image import ImageManager
from bot.misc import Config, Env
from bot.misc.util import random_packet, import_module


class __MainOtherCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        text = self.bot.get_channel(Env.CHANNEL)
        if Env.THREAD != "nan":
            text = text.get_thread(Env.THREAD)
        Env.Server = Server(self.bot.get_channel(Env.VOICE), text)
        for filename in os.listdir("bot/packets"):
            if filename.endswith(".py") and not filename.startswith("__"):
                module = import_module(filename[:-3], "bot/packets")
                if module.info().countPlayers <= len(Env.Server.guild.emojis):
                    Env.Packets.append(module)
        Env.ImageManager = ImageManager(self.bot.user.avatar.url, Env.Server.guild.icon.url)
        await random_packet(Env.Packets, Env.Server, Config.DEBUG_MODE, Env.ImageManager)
        Env.Role = discord.utils.get(Env.Server.guild.roles, id=Env.ROLE_ID)
        if len(Env.Server.voice.members) == Env.Server.voice.user_limit:
            self.bot.dispatch("start_game")


async def register_other_cogs(bot: Bot) -> None:
    await bot.add_cog(__MainOtherCog(bot))
