from typing import Dict, List
from dataclasses import dataclass
from uuid import UUID
import numpy as np
from numpy.random import default_rng

@dataclass
class Tile():
    id: UUID
    contents: List[str]

@dataclass
class TileSet():
    # id: str
    # tile: Dict(UUID, Tile)
    # TODO do we need these? If so, pull from setup parameters
    lowerRange = 1
    upperRange = 10

    def getRandomTiles(self, num: int) -> List[Tile]: # and have no duplicates on each board
        # np.random.randint(lowInt, highInt, )
        rng = default_rng()
        try:
            numbers = rng.choice(np.arange(self.lowerRange,self.upperRange), size=num, replace=False)
            print(numbers)
            return numbers
        except ValueError:
            print("Too many unique numbers requested for range! Increase range and try again")
            self.upperRange = int(input("New value for upper limit of range: "))
            self.getRandomTiles(num)

@dataclass
class DataStorage():
    # TileSets: Dict[str, TileSet]

    def getTile(self, id: UUID) -> Tile:
        pass

    def getTileSet(self, name: str) -> TileSet:
        pass

    def addTile(self, contents: str, tileset: str = None) -> bool:
        pass

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        pass