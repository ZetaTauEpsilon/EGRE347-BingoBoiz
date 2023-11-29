import data
import json

with open('tileset.json') as tileset_json:
    tileset = json.load(tileset_json)

with open('tile.json') as tile_json:
    tile = json.load(tile_json)

mainData = data.DataStorage(tileset)

mainData.addTileSet("StarWars", ['ObiWan', 'Luke', 'Darth Vader'])

# TestTileSet = data.TileSet("TestID", tile=tile)

# TestTileSet.helper()

# TileList = TestTileSet.getRandomTiles(2)

# print(TileList)

