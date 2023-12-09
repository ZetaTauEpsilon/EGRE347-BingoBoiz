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
        colData = ()
        for row in playerBoard.state:
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
    def checkLtRDiagonalWin(self, playerBoard):
        count, itr = 0
        while itr < playerBoard.size:
            if playerBoard.state[count][count]:
                count += 1
            itr += 1
        return True if count == playerBoard.size else False
    
    # Check right-left diagonal
    def checkRtLDiagonalWin(self, playerBoard):
        countX = playerBoard.size - 1
        countY, itr = 0
        count = 0
        while itr < playerBoard.size:
            if playerBoard.state[countX][countY]:
                count += 1
            itr += 1
            countX -= 1
            countY += 1
        return True if count == playerBoard.size else False
        
    def evaluateWin(self, BoardState: BoardState, tileX, tileY) -> bool:
        """Inputs: Tile Coordinates"""
        # Run this function every time a tile state is changed
        # Check if the tile is on one of the diagonals
        # Check the column and row where the tile state was changed
        # If the tile is on one of the diagonals check them
        # If all tile states in the column or row or diagonal are true,
        # then return a win       
        if self.checkLtRDiagonalWin(BoardState) | self.checkRtLDiagonalWin(BoardState):
            return True 
        col = self.grabCol(BoardState, tileX)
        if self.checkWinHV(col) | self.checkWinHV(BoardState.state[tileY]):
            return True
        else:
            return False