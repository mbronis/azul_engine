"""Represents game tiles."""
from typing import Optional, List
from enum import Enum


class Tile(Enum):
    BLUE = "U"
    YELLOW = "Y"
    RED = "R"
    BLACK = "B"
    SNOW = "S"


WallTiles = List[List[Optional[Tile]]]
