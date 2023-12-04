class Player():

    def __init__(self, pid, name, board):
        self.id = pid
        self.name = name
        self.wins = 0
        self.board = board

    def addWin(self) -> bool:
        pass