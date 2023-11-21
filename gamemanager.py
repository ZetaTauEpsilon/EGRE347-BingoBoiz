from lobby import Lobby
from json import JSON


class GameManager():

    def __init__():
        pass

    def makeBoard(Lobby: Lobby) -> JSON:
        pass
        """Inputs: TileSet, IsFreeEnabled"""
        # Create a 2D array from a list of tiles depending on the set
        # Set the middle tile to free if its enabled

    def evaluateWin(BoardState: BoardState) -> bool:
        pass
        """Inputs: Tile Coordinates"""
        # Run this function every time a tile state is changed
        # Check if the tile is on one of the diagonals
        # Check the column and row where the tile state was changed
        # If the tile is on one of the diagonals check them
        # If all 5 tile states in the column or row or diagonal are true,
        # then return a win