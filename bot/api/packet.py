from bot.misc.locale import Locale


class Packet:
    id: str
    name: str
    roles: tuple
    teams: tuple
    countPlayers: int
    timing: (int, int)  # 0 - day, 1 - night

    def __init__(self, ID: str, name: str, countPlayers: int, timing: (int, int)):
        self.id = ID
        self.name = name
        self.countPlayers = countPlayers
        self.timing = timing

    def info(self):
        return Locale.PacketInfo.format(self.name, self.timing[0], self.timing[1])
