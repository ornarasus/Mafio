import discord

from bot.api.packet import Packet
from bot.api.player import Player
from bot.misc.env import Env


class Server:
    packet: Packet | None
    isPlaying: bool
    voice: discord.VoiceChannel
    guild: discord.Guild
    text: discord.TextChannel | discord.Thread
    players: list
    isNight: bool
    liveTeams: list
    buffer: list
    messages: list

    def __init__(self, voice: discord.VoiceChannel, text: discord.TextChannel | discord.Thread):
        self.isPlaying = False
        self.packet = None
        self.version = None
        self.isNight = True
        self.players = list()
        self.messages = [[], []]
        self.guild = voice.guild
        self.voice = voice
        self.text = text

    async def killPlayer(self, player: Player):
        await player.member.remove_roles(Env.Role)
        self.players.remove(player)
        if player.member.id in self.messages[0]:
            i = self.messages[0].index(player.member.id)
            self.messages[1].pop(i)
            self.messages[0].pop(i)

    def getCountLiveTeams(self) -> int:
        self.liveTeams = list(set([player.role.teamID for player in self.players]))
        return len(self.liveTeams)

    def hadPlayer(self, member: discord.Member) -> bool:
        return discord.utils.get(self.players, member=member) is not None
