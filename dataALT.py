from typing import Dict, List
from dataclasses import dataclass
from uuid import UUID, uuid1
import numpy as np
from numpy.random import default_rng
import json

#**************************************
debug = 1
#**************************************

class Tile():
    def __init__(self, tile):
        self.id = tile["id"]
        self.contents = tile["contents"]
    # id: UUID
    # contents: List[str]
    


class TileSet():
    def __init__(self, tilesetIn) -> None:
        self.tilesetOut = []
        self.name = tilesetIn["id"]
        for tile in tilesetIn['tile']:
            self.tilesetOut.append(Tile(tilesetIn['tile'][tile]))

    # def addSet(self, name: str, ids: List[str]):
    #     # print(type(self.tile))
    #     self.tile["id"] = name
    #     self.tile["content"] = Tile(self.id, ids)



class DataStorage():

    def __init__(self, filename : str) -> None:
        self.TileSets = {}
        with open(filename) as tilesets_json:
            tilesets= json.load(tilesets_json)
        
            for tileset in tilesets:
                self.TileSets[tileset['id']] = TileSet(tileset)

    # @classmethod
    # def fromTileSets(self, tileset : dict[str, TileSet]):
    #     self.TileSets = tileset

    # def getTile(self, id: UUID) -> Tile:
    #     pass

    def getTileSet(self, name: str) -> TileSet:
        return self.TileSets[name]

    def addTile(self, contents: List[str], tilesetName: str = None) -> bool:
        try:
            tempID = uuid1()
            self.TileSets[tilesetName].tile[tempID] = Tile({"id" : tempID, "contents" : contents})
            return True
        except KeyError:
            print("Tileset does not exist")
            return False
        

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        self.TileSets[name] = TileSet({"id" : name, "tile" : {}})
        return True


# def init(tile_json : str, tileset_json : str) -> DataStorage:
    
#     D = DataStorage()
    
    


    # with open('tileset.json') as tileset_json:
    #     tileset = json.load(tileset_json)
    #     ran = True
    #     for tl in tileset:
    #         if ran:
    #             D = DataStorage(tl).addTileSet(tl["id"], tl["tile"])
    #         # else:
    #             # D = DataStorage(tl)
    #         # ran = True
    

    # return D

D = DataStorage('tileset.json')

print(D.getTileSet('tileset2').name)



