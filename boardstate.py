
class BoardState:
    
    def __init__(self):
        self.state
        self.contents

    def updateState(self, row, col) -> bool:
        if(self.state[row][col] == False):
            self.state[row][col] = True
        else:
            self.state[row][col] = False
    """Inputs: Row and Column of Tile"""
    # Change the state of the tile at given coordinates
    # Based on the current state of the tile