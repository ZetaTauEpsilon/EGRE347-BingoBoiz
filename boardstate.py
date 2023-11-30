
class BoardState:
    
    def __init__(self):
        self.state
        self.contents

    def updateState(self, row, col) -> bool:
        self.state[row][col] = True if self.state[row][col] == False else False
    """Inputs: Row and Column of Tile"""
    # Change the state of the tile at given coordinates
    # Based on the current state of the tile