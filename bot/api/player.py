import discord

from bot.api.role import Role


class Player:
    role: Role
    member: discord.Member
    emoji: discord.Emoji

    def __init__(self, member: discord.Member, emoji: discord.Emoji, role: Role):
        self.member = member
        self.emoji = emoji
        self.role = role
