from dataclasses import dataclass

from src.env.tiles import Tile


@dataclass
class AddWallTile:
    row: int
    col: int
    tile: Tile
