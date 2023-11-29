from typing import Dict, List
from dataclasses import dataclass
from uuid import UUID
import numpy as np
from numpy.random import default_rng
import json

#**************************************
debug = 1
#**************************************

@dataclass
class Tile():
    id: UUID
    contents: List[str]
    

@dataclass
class TileSet():
    id: str
    tile: dict["id": UUID, "contents" : Tile]

    def helper(self):
        pass
    
    # TODO do we need these? If so, pull from setup parameters
    lowerRange = 1
    upperRange = 100

    def getRandomTiles(self, num: int) -> List[Tile]: # and have no duplicates on each board

        rng = default_rng()
        TileList:List[Tile] = []
       
        try:
            numbers = rng.choice(np.arange(self.lowerRange,self.upperRange), size=num, replace=False)
            if debug: print(numbers)
            for number in numbers:
                TileList.append(Tile("TEST_UUID", str(number)))
            return TileList
        
        except ValueError:
            self.upperRange = num + 1
            self.getRandomTiles(num)

    def addSet(self, name: str, tiles: List[str]):
        self.tile["id"].append(name)
        self.tile["contents"] = Tile(self.id, tiles)


@dataclass
class DataStorage():
    TileSets: dict[str, TileSet]

    def getTile(self, id: UUID) -> Tile:
        pass

    def getTileSet(self, name: str) -> TileSet:
        pass

    def addTile(self, contents: str, tileset: str = None) -> bool:
        pass

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        print (type(self.TileSets))
        TileSet(name, self.TileSets).addSet(name, tiles)
        return True
