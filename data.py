from typing import dataclass, Dict, List
from uuid import UUID

@dataclass
class Tile():
    id: UUID
    contents: List[str]

@dataclass
class TileSet():
    id: str
    tile: Dict(UUID, Tile)

    def getRandomTiles(num: int) -> List[Tile]:
        pass

@dataclass
class DataStorage():
    TileSets: Dict[str, TileSet]

    def getTile(self, id: UUID) -> Tile:
        pass

    def getTileSet(self, name: str) -> TileSet:
        pass

    def addTile(self, contents: str, tileset: str = None) -> bool:
        pass

    def addTileSet(self, name: str, tiles: List[str]) -> bool:
        pass