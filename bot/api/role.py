class Role:
    name: str
    description: str
    teamID: int
    countPlayers: int

    def __init__(self, name: str, teamID: int, countPlayers: int, description: str):
        self.name = name
        self.description = description
        self.teamID = teamID
        self.countPlayers = countPlayers
