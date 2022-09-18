import discord

from bot.misc.util import get_nick
from bot.api.server import Server
from bot.api.role import Role
from bot.api.packet import Packet


def info() -> Packet:
    packet = Packet(str(__file__)[:-3], "Классическая мафия", 10, (30, 15))
    packet.teams = ("Жители", "Мафия")
    packet.roles = (Role("Мирный житель", 0, 6, "Ночью видит сны"),
                    Role("Мафия", 1, 2, "Ночью выбирают в кого стрелять"),
                    Role("Шериф", 0, 1, "Проверяет любого игрока в причастности к мафии"),
                    Role("Дон", 1, 1, "Проверяет любого игрока в причастности к полиции"))
    return packet


async def main(buffer: list, game: Server) -> list:
    maf = await voteMafia(buffer, game)
    await checkTeam(buffer, game)
    data = [f'Мафия застрелила игрока "{get_nick(maf)}"'
            if maf is not None else "Мафия никого не застрелила!"]
    return data


async def voteMafia(buffer: list, game: Server) -> discord.Member | None:
    if len(buffer[0][1]) > 0:
        counts = {buffer[0][1].count(i): i for i in buffer[0][1]}
        member = counts[max([c for c in counts.keys()])]
        player = discord.utils.get(game.players, member=member)
        await game.killPlayer(player)
        return member
    else:
        return None


async def checkTeam(buffer: list, game: Server):
    member = buffer[0][2][0]
    player = discord.utils.get(game.players, member=member)
    self = discord.utils.get(game.players, member=buffer[1][2][0])
    await self.member.sendMessage(f'Игрок {get_nick(member)} '
                                  f'{"" if player.role.teamID != 0 else "не "} '
                                  f'является членом Мафии')
    member = buffer[0][3][0]
    player = discord.utils.get(game.players, member=member)
    self = discord.utils.get(game.players, member=buffer[1][3][0])
    await self.member.sendMessage(f'Игрок {get_nick(member)} '
                                  f'{"" if player.role.teamID != 0 else "не "} '
                                  f'является Шерифом')
