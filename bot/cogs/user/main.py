import discord
from discord.ext.commands import Cog, Bot


from bot.misc import Env
from bot.misc.locale import Locale
from bot.misc.util import get_nick


class __MainUserCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None:
            if before.channel == Env.Server.voice:
                if Env.Server.hadPlayer(member):
                    await Env.Server.killPlayer(discord.utils.get(Env.Server.players, member=member))
                    if Env.Server.getCountLiveTeams() <= 1:
                        Env.LoopTask.cancel()
                        self.bot.dispatch("stop_game")
        if after.channel is not None:
            if after.channel == Env.Server.voice:
                if after.channel.user_limit == len(after.channel.members):
                    self.bot.dispatch("start_game")

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id in Env.Server.messages[0]:
            if reaction.message.id in Env.Server.messages[1]:
                member = discord.utils.get(Env.Server.guild.members, id=user.id)
                player = discord.utils.get(Env.Server.players, member=member)
                target = discord.utils.get(Env.Server.players, emoji=reaction.emoji)
                if Env.Server.isNight:
                    indexPlayer = Env.Server.packet.roles.index(player.role)
                    Env.Server.buffer[0][indexPlayer].append(target.member)
                    Env.Server.buffer[1][indexPlayer].append(member)
                else:
                    Env.Server.buffer[0].append(target.member)
                    Env.Server.buffer[1].append(member)
                await reaction.message.delete()
                text = Locale.Voted.format(get_nick(target.member))
                with Env.ImageManager.info(text) as endVote:
                    mess = await user.send(file=discord.File(fp=endVote, filename="endVote.png"))
                Env.Server.messages[1][Env.Server.messages[0].index(user.id)] = mess.id


async def register_user_cogs(bot: Bot) -> None:
    await bot.add_cog(__MainUserCog(bot))
