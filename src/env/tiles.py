"""Represents game tiles."""
from typing import Optional, List
from enum import Enum, auto


class Tile(Enum):
    BLUE = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()
    SNOW = auto()


WallTiles = List[List[Optional[Tile]]]
