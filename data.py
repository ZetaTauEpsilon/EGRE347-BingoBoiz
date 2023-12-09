from typing import Dict, List
from dataclasses import dataclass
from uuid import UUID, uuid1
# import numpy as np
# from numpy.random import default_rng
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
        self.tiles = []
        self.name = tilesetIn["id"]
        for tile in tilesetIn['tile']:
            self.tiles.append(Tile(tilesetIn['tile'][tile]))


    # def getIDs(self, tileSetName):
    #     pass

class DataStorage():
    def __init__(self, filename : str) -> None:
        self.TileSets = {}
        with open(filename) as tilesets_json:
            tilesets= json.load(tilesets_json)
            self.filename = filename
        
            for tileset in tilesets:
                self.TileSets[tileset['id']] = TileSet(tileset)

    def getTileSet(self, name: str) -> TileSet:
        return self.TileSets[name]
    
    def getTileSetIDs(self, tilesetName : str):
        ids = []
        tileset = self.getTileSet(tilesetName)
        for tile in tileset.tiles:
            ids.append(tile.id)
        return ids

    def addTile(self, contents: str, tilesetName: str = None) -> bool:
        try:
            tempID = str(uuid1())
            self.TileSets[tilesetName].tiles.append(Tile({"id" : tempID, "contents" : contents}))
            return True
        except KeyError:
            print("Tileset does not exist")
            return False
        

    def addTileSet(self, name: str, tiles: str) -> bool:
        '''
        Check if tileset already exits, if so append
        If not, create a new tileset
        '''
        res = list(map(str.strip, tiles.split(',')))

        tileSetExists = False
        for tileSetName in self.TileSets:
            if tileSetName == name:
                tileSetExists = True
        if not tileSetExists:
            self.TileSets[name] = TileSet({"id" : name, "tile" : {}})
        
        for tile in res:
            self.addTile(tile, name)

        self.dumpToJSON()
        
        return True

    def dumpToJSON (self) -> bool:
        dictList = []
        for key in self.TileSets.keys():
            new = {}
            new['id'] = key
            new['tile'] = {}
            for tile in self.TileSets[key].tiles:
                new['tile'][tile.id] = {"id": tile.id, "contents": tile.contents} 
            dictList.append(new)
        
        # Serializing json
        json_object = json.dumps(dictList, indent=4)
        
        # Writing to sample.json
        with open(self.filename, "w") as outfile:
            outfile.write(json_object)
        return True

# D = DataStorage('tileset.json')
# D.addTileSet('test', 'here, is, a, new, tileset')

# D.dumpToJSON()

# print(D.getTileSetIDs('tileset2'))

