from lobby import Lobby
from json import JSON
import random
from boardstate import BoardState


class GameManager():

    def __init__():
        pass

    def makeBoard(Lobby: Lobby, tileSet, isFreeEnabled, boardSize) -> JSON:
        board = [[0 for i in range(boardSize)] for j in range(boardSize)]
        state = [[False for i in range(boardSize)] for j in range(boardSize)]
        tileSampleSize = boardSize*boardSize
        availableTiles = random.sample(tileSet, tileSampleSize)
        tileCt = 0
        for row in boardSize:
            for col in boardSize:
                board[row][col] = availableTiles[tileCt]
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
                board[randRow][randCol] = "Free"
                state[randRow][randCol] = True
            else:
                center = round(boardSize/2) + 1
                board[center][center] = "Free"
                state[center][center] = True

    def evaluateWin(BoardState: BoardState, tileX, tileY) -> bool:
        pass
        """Inputs: Tile Coordinates"""
        # Run this function every time a tile state is changed
        # Check if the tile is on one of the diagonals
        # Check the column and row where the tile state was changed
        # If the tile is on one of the diagonals check them
        # If all 5 tile states in the column or row or diagonal are true,
        # then return a win