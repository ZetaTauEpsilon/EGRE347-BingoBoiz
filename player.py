from uuid import UUID, uuid1

class Player():
    def __init__(self, pid, name, board):
        self.id = pid
        self.name = name
        self.wins = 0
        self.board = board

    def addWin(self) -> bool:
        self.numWins += 1
        return True