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
    tile: dict[UUID, Tile]

    # TODO do we need these? If so, pull from setup parameters
    lowerRange = 1
    upperRange = 100

    def getRandomTiles(self, num: int) -> List[Tile]: # and have no duplicates on each board
        if(id == 0):
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
        else:
            TileList:List[Tile] = []
            # TODO add functionality

    def addSet(self, name: str, tiles: List[str]):
        # print(type(self.tile))
        self.tile["id"] = name
        self.tile["contents"] = Tile(self.id, tiles)


@dataclass
class DataStorage():
    TileSets: dict[str, TileSet]

    def getTile(self, id: UUID) -> Tile:
        print(self.TileSets[id])
        pass

    def getTileSet(self, name: str) -> TileSet:
        print(type(self.TileSets[name]))

    def addTile(self, contents: str, tileset: str = None) -> bool:
        pass

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        self.TileSets["id"] = name
        self.TileSets["tile"] = TileSet(name, self.TileSets).addSet(name, tiles)
        # print(self.TileSets)
        return True



def init(tile_json : str, tileset_json : str) -> DataStorage:
    with open('tile.json') as tile_json:
        tile = json.load(tile_json)
        for t in tile:
            T = Tile(t["id"], t["contents"])

    with open('tileset.json') as tileset_json:
        tileset = json.load(tileset_json)
        ran = False
        for tl in tileset:
            if ran:
                D.addTileSet(tl["id"], tl["tile"])
            else:
                D = DataStorage(tl)
            ran = True
    return D
    