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


class TileSet():
    def __init__(self, tilesetIn) -> None:
        self.tilesetOut = []
        self.name = tilesetIn["id"]
        for tile in tilesetIn['tile']:
            self.tilesetOut.append(Tile(tilesetIn['tile'][tile]))


class DataStorage():

    def __init__(self, filename : str) -> None:
        self.TileSets = {}
        with open(filename) as tilesets_json:
            tilesets= json.load(tilesets_json)
        
            for tileset in tilesets:
                self.TileSets[tileset['id']] = TileSet(tileset)

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

# D = DataStorage('tileset.json')

# print(D.getTileSet('tileset2').name)