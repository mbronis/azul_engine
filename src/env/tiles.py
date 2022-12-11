"""Represents game tiles."""
from typing import Optional, List
from enum import Enum


class Tile(Enum):
    BLUE = "u"
    YELLOW = "y"
    RED = "r"
    BLACK = "b"
    SNOW = "s"


WallTiles = List[List[Optional[Tile]]]
