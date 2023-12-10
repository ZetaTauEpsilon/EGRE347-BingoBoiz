import random
from boardstate import BoardState
from data import Tile


class GameManager():

    def __init__(self, size):
        self.board = []
        self.state = []
        self.size = size

    def makeBoard(self, Lobby, tileSet, isFreeEnabled, boardSize):
        self.size = boardSize
        self.board = [[0 for i in range(boardSize)] for j in range(boardSize)]
        self.state = [[False for i in range(boardSize)] for j in range(boardSize)]

        sample = random.sample(tileSet.tiles, boardSize**2)

        for row in range(boardSize):
            for col in range(boardSize):
                choice = random.choice(sample)
                self.board[row][col] = Tile({"id": choice.id, "contents": random.choice(choice.contents)})
                sample.remove(choice)

        """Inputs: TileSet, IsFreeEnabled"""
        # Create a 2D array from a list of tiles depending on the set
            # Loop that selects a random tile from the set and puts it into the 
        # Set the middle tile to free if its enabled
        if(isFreeEnabled):
            if boardSize % 2 == 0:
                # choose random tile
                randCol = random.randrange(boardSize-1)
                randRow = random.randrange(boardSize-1)
                self.board[randRow][randCol] = Tile({"id":"free","contents": "Free"})
                self.state[randRow][randCol] = True
            else:
                center = round(boardSize/2)
                self.board[center][center] = Tile({"id":"free","contents": "Free"})
                self.state[center][center] = True
        return BoardState(self.state, self.board)

    def grabCol(self, playerBoard, col):
        for row in playerBoard.state:
            yield row[col]

    def grabRow(self, playerBoard, row):
        return playerBoard.state[row]

    # Check column and row
    def checkWinHV(self, l):
        for item in l:
            if item == True:
                continue
            else:
                return False
        return True
        
    def evaluateWin(self, bs: BoardState, tileX, tileY) -> bool:
        """Inputs: Tile Coordinates"""
        # Run this function every time a tile state is changed
        # Check if the tile is on one of the diagonals
        # Check the column and row where the tile state was changed
        # If the tile is on one of the diagonals check them
        # If all tile states in the column or row or diagonal are true,
        # then return a win       
        col = list(self.grabCol(bs, tileX))
        row = list(self.grabRow(bs, tileY))

        if self.checkWinHV(row):
            return True
        
        if self.checkWinHV(col):
            return True

        if tileX == tileY:
            for i in range(len(bs.state)):
                if bs.state[i][i] == True:
                    continue
                else:
                    return False
                return True
        
        if tileX + tileY == len(bs.state) - 1:
            for i in range(len(bs.state)):
                if bs.state[i][len(bs.state) - 1 - i] == True:
                    continue
                else:
                    return False
                return True
        
        return False