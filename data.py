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
    # lowerRange = 1
    # upperRange = 100

    # def getRandomTiles(self, num: int) -> List[Tile]: # and have no duplicates on each board
    #     if(id == 0):
    #         rng = default_rng()
    #         TileList:List[Tile] = []
    #         try:
    #             numbers = rng.choice(np.arange(self.lowerRange,self.upperRange), size=num, replace=False)
    #             if debug: print(numbers)
    #             for number in numbers:
    #                 TileList.append(Tile("TEST_UUID", str(number)))
    #             return TileList

    #         except ValueError:
    #             self.upperRange = num + 1
    #             self.getRandomTiles(num)
    #     else:
    #         TileList:List[Tile] = []
    #         # TODO add functionality

    def addSet(self, name: str, tiles: List[str]):
        # print(type(self.tile))
        self.tile["id"] = name
        self.tile["contents"] = Tile(self.id, tiles)



class DataStorage():

    def __init__(self) -> None:
        self.TileSets = {'name' : 'bufferData', 'tileSet' : TileSet('randomID', Tile('testTileID', ['testContents']))}
        print(type(self.TileSets))
        # with open('result1.json', 'w') as fp:
        #     json.dump(self.TileSets, fp)
        # return True
        pass
    
    @classmethod
    def fromTileSets(self, tileset : dict[str, TileSet]):
        self.TileSets = tileset

    def getTile(self, id: UUID) -> Tile:
        print(self.TileSets[id])
        pass

    def getTileSet(self, name: str) -> TileSet:
        # print(self.TileSets[name])
        pass

    def addTile(self, contents: str, tileset: str = None) -> bool:
        T = Tile(str, contents)
        # print(type(self.TileSets))
        self.TileSets[tileset]['contents'] = contents
        return True

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        print(type(self.TileSets))
        self.TileSets['id'] = name
        self.TileSets['tile'] = TileSet(name, self.TileSets).addSet(name, tiles)
        # print(self.TileSets)

        # with open('result.json', 'w') as fp:
        #     json.dump(self.TileSets, fp)
        # return True



def init(tile_json : str, tileset_json : str) -> DataStorage:
    
    D = DataStorage()
    
    with open('tile.json') as tile_json:
        tile = json.load(tile_json)
        
        for t in tile:
            # T = Tile(t["id"], t["contents"])
            D.addTile(t['contents'], t['id'])


    # with open('tileset.json') as tileset_json:
    #     tileset = json.load(tileset_json)
    #     ran = True
    #     for tl in tileset:
    #         if ran:
    #             D = DataStorage(tl).addTileSet(tl["id"], tl["tile"])
    #         # else:
    #             # D = DataStorage(tl)
    #         # ran = True
    

    return D
    