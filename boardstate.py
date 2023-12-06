from data import Tile

class BoardState:
    def __init__(self, size):
        self.state = [[0 for x in range(size)] for y in range(size)]
        self.contents = [[Tile({"id": "123123", "contents": "asdf"}) for x in range(size)] for y in range(size)]

    def updateState(self, row, col) -> bool:
        self.state[row][col] = True if self.state[row][col] == False else False
    """Inputs: Row and Column of Tile"""
    # Change the state of the tile at given coordinates
    # Based on the current state of the tile