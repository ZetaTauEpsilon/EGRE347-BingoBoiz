from typing import Dict, List
from dataclasses import dataclass
from uuid import UUID, uuid1
import json

class Tile():
    '''
    UUID for each Tile
    Contents stored as string
    '''
    def __init__(self, tile):
        self.id = tile["id"]
        self.contents = tile["contents"]

class TileSet():
    '''
    Store tiles as List of Tile objects
    Create UUID for TileSet
    '''
    def __init__(self, tilesetIn) -> None:
        self.tiles = []
        self.name = tilesetIn["id"]
        for tile in tilesetIn['tile']:
            self.tiles.append(Tile(tilesetIn['tile'][tile]))

class DataStorage():
    '''
    Object that stores Tile and TileSet objects
    Items accessible through getters and setters
    '''
    def __init__(self, filename : str) -> None:
        '''
        Open JSON and comprehend dictionary
        '''
        self.TileSets = {}
        with open(filename) as tilesets_json:
            tilesets= json.load(tilesets_json)
            self.filename = filename
        
            for tileset in tilesets:
                self.TileSets[tileset['id']] = TileSet(tileset)

    def getTileSet(self, name: str) -> TileSet:
        '''
        Return TileSet object based on string name
        '''
        return self.TileSets[name]
    
    def getTileSetIDs(self, tilesetName : str):
        '''
        Get Tile UUIDs for specified TileSet
        '''
        ids = []
        tileset = self.getTileSet(tilesetName)
        for tile in tileset.tiles:
            ids.append(tile.id)
        return ids

    def addTile(self, contents: str, tilesetName: str = None) -> bool:
        '''
        Creates UUID
        Assigns Tile object to TileSet
        '''
        try:
            tempID = str(uuid1())
            self.TileSets[tilesetName].tiles.append(Tile({"id" : tempID, "contents" : contents}))
            return True
        except KeyError:
            print("TileSet does not exist")
            return False
        

    def addTileSet(self, name: str, tiles: str) -> bool:
        '''
        Check if tileset already exits, if so append tiles to it
        If not, create a new TileSet
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

        return True
    def dumpToJSON (self) -> bool:
        '''
        Transfer out of our storage method back to JSON
        Dumps back into original file
        '''
        dictList = []
        for key in self.TileSets.keys():
            new = {}
            new['id'] = key
            new['tile'] = {}
            for tile in self.TileSets[key].tiles:
                new['tile'][tile.id] = {"id": tile.id, "contents": tile.contents} 
            dictList.append(new)

        json_object = json.dumps(dictList, indent=4)

        with open(self.filename, "w") as outfile:
            outfile.write(json_object)
        return True