import data
import json

with open('tileset.json') as tileset_json:
    tile = json.load(tileset_json)

TestTileSet = data.TileSet("TestID", tile=tile)

TileList = TestTileSet.getRandomTiles(15)

print(TileList)

