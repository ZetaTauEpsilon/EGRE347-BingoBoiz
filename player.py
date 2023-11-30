from uuid import UUID, uuid1

class Player():

    def __init__(self, playerName : str):
        self.id = uuid1()
        self.name = playerName
        self.numWins = 0

    def addWin(self) -> bool:
        self.numWins += 1
        return True