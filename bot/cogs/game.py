import asyncio

import discord
from discord.ext.commands import Bot, Cog

from bot.api.player import Player
from bot.misc import Env, Config
from bot.misc.locale import Locale
from bot.misc.util import random_roles, random_emojis, get_nick, random_packet


class __MainGameCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_start_game(self):
        roles = random_roles(Env.Server.packet.roles)
        emojis = random_emojis(Env.Server.packet.countPlayers, Env.Server.guild.emojis)
        for i in range(len(Env.Server.voice.members)):
            member = Env.Server.voice.members[i]
            player = Player(member, emojis[i], roles[i])
            Env.Server.players.append(player)
            await member.add_roles(Env.Role)
            text = Locale.RoleInfo.format(Env.Server.guild.name,
                                          Env.Server.packet.name, player.role.name)
            with Env.ImageManager.info(text) as role:
                await member.send(file=discord.File(fp=role, filename="role.png"))
        await Env.Server.voice.set_permissions(Env.Server.guild.default_role, connect=False)
        Env.Server.isPlaying = True
        Env.LoopTask = asyncio.Task(self.loop_game())

    async def loop_game(self):
        abilities = Env.Server.version
        while Env.Server.getCountLiveTeams() > 1:
            Env.Server.messages = [[], []]
            await Env.Server.voice.set_permissions(Env.Role, speak=not Env.Server.isNight)
            Env.Server.buffer = [[], []]
            if Env.Server.isNight:
                for i in range(len(Env.Server.packet.roles)):
                    Env.Server.buffer[0].append([])  # target
                    Env.Server.buffer[1].append([])  # self
            dataVote = dict()
            for player in Env.Server.players:
                dataVote.update({get_nick(player.member): player.emoji.url})
            for player in Env.Server.players:
                user = await self.bot.fetch_user(player.member.id)
                if not (Env.Server.isNight and player.role == Env.Server.packet.roles[0]):
                    text = Locale.Night if Env.Server.isNight else Locale.Day
                    with Env.ImageManager.vote(text, dataVote) as vote:
                        message = await user.send(file=discord.File(vote, "vote.png"))
                    for pl in Env.Server.players:
                        await message.add_reaction(pl.emoji)
                    Env.Server.messages[1].append(message.id)
                else:
                    with Env.ImageManager.info(Locale.NightCitizen) as vote:
                        await user.send(file=discord.File(vote, "vote.png"))
                    Env.Server.messages[1].append(None)
                Env.Server.messages[0].append(user.id)
            await asyncio.sleep(Env.Server.packet.timing[Env.Server.isNight])
            if Env.Server.isNight:
                data = await abilities.main(Env.Server.buffer, Env.Server)
                with Env.ImageManager.resultNight(data) as result:
                    await Env.Server.text.send(file=discord.File(result, "resultNight.png"))
            else:
                if len(Env.Server.buffer[0]) > 0:
                    counts = {Env.Server.buffer[0].count(i): i for i in Env.Server.buffer[0]}
                    member = counts[max([c for c in counts.keys()])]
                    player = discord.utils.get(Env.Server.players, member=member)
                    text = Locale.EndDay.format(get_nick(player.member), player.role.name)
                    with Env.ImageManager.info(text) as endDay:
                        await Env.Server.text.send(file=discord.File(fp=endDay, filename="endDay.png"))
                    await Env.Server.killPlayer(player)
            Env.Server.isNight = not Env.Server.isNight
        self.bot.dispatch("stop_game")

    @Cog.listener()
    async def on_stop_game(self):
        Env.LoopTask = None
        text = Locale.WinInfo.format(Env.Server.packet.teams[Env.Server.liveTeams[0]])
        with Env.ImageManager.info(text) as endGame:
            await Env.Server.text.send(file=discord.File(fp=endGame, filename="endGame.png"))
        await Env.Server.voice.set_permissions(Env.Server.guild.default_role, connect=True)
        for pl in Env.Server.players:
            await Env.Server.killPlayer(pl)
        Env.Server.isPlaying = False
        await random_packet(Env.Packets, Env.Server, Config.DEBUG_MODE, Env.ImageManager)
        for i in Env.Server.voice.members:
            await i.move_to(Env.Server.guild.get_channel(Env.AFK) if Config.DEBUG_MODE else None)


async def register_game_cogs(bot: Bot) -> None:
    await bot.add_cog(__MainGameCog(bot))
