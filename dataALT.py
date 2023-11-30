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
    


class TileSet():
    def __init__(self, id : str, tile : dict[UUID, Tile]) -> None:
        self.id = id
        self.tile = tile

    def addSet(self, name: str, ids: List[str]):
        # print(type(self.tile))
        self.tile["id"] = name
        self.tile["content"] = Tile(self.id, ids)



class DataStorage():

    def __init__(self) -> None:
        self.TileSets = {'name' : 'bufferData', 'tileSet' : TileSet('randomID', Tile('testTileID', ['testContents']))}

    @classmethod
    def fromTileSets(self, tileset : dict[str, TileSet]):
        self.TileSets = tileset

    def getTile(self, id: UUID) -> Tile:
        pass

    def getTileSet(self, name: str) -> TileSet:
        pass

    def addTile(self, contents: str, tileset: str = None) -> bool:
        T = Tile("SAMPLE_UUID", contents)
        try:
            self.TileSets[tileset]['content'] = contents
        except KeyError:
            print("Tileset does not exist")
        return True

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        pass


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
    