from lobby import Lobby
from json import JSON
import random
from boardstate import BoardState


class GameManager():

    def __init__(self):
        self.board
        self.state
        self.size

    def makeBoard(self, Lobby: Lobby, tileSet, isFreeEnabled, boardSize) -> JSON:
        self.size = boardSize
        self.board = [[0 for i in range(boardSize)] for j in range(boardSize)]
        self.state = [[False for i in range(boardSize)] for j in range(boardSize)]
        tileSampleSize = boardSize*boardSize
        availableTiles = random.sample(tileSet.tiles, tileSampleSize)
        tileCt = 0
        for row in boardSize:
            for col in boardSize:
                self.board[row][col] = availableTiles[tileCt]
        """Inputs: TileSet, IsFreeEnabled"""
        # Create a 2D array from a list of tiles depending on the set
            # Loop that selects a random tile from the set and puts it into the 
        # Set the middle tile to free if its enabled
        if(isFreeEnabled):
            isEven = True if boardSize % 2 == 0 else False
            if(isEven):
                # choose random tile
                randCol = random.randrange(boardSize-1)
                randRow = random.randrange(boardSize-1)
                self.board[randRow][randCol] = "Free"
                self.state[randRow][randCol] = True
            else:
                center = round(boardSize/2) + 1
                self.board[center][center] = "Free"
                self.state[center][center] = True

    def grabCol(self, col):
        colData = ()
        for row in self.state:
            for item in row:
                if row.index(item) == col:
                    colData.append(item)
        return colData 

    # Check column and row
    def checkWinHV(self, col):
        count = 0
        for item in col:
            if item:
                count += 1
        return True if count == len(col) else False

    # Check left-right diagonal
    def checkLtRDiagonalWin(self):
        count, itr = 0
        while itr < self.size:
            if self.state[count][count]:
                count += 1
            itr += 1
        return True if count == self.size else False
    
    # Check right-left diagonal
    def checkRtLDiagonalWin(self):
        countX = self.size - 1
        countY, itr = 0
        count
        while itr < self.size:
            if self.state[countX][countY]:
                count += 1
            itr += 1
            countX -= 1
            countY += 1
        return True if count == self.size else False
        
    def evaluateWin(self, BoardState: BoardState, tileX, tileY) -> bool:
        """Inputs: Tile Coordinates"""
        # Run this function every time a tile state is changed
        # Check if the tile is on one of the diagonals
        # Check the column and row where the tile state was changed
        # If the tile is on one of the diagonals check them
        # If all tile states in the column or row or diagonal are true,
        # then return a win       
        if self.checkLtRDiagonalWin() | self.checkRtLDiagonalWin():
            return True 
        col = self.grabCol(tileX)
        if self.checkWinHV(col) | self.checkWinHV(self.state[tileY]):
            return True
        else:
            return False