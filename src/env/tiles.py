"""Represents game tiles."""
from typing import Optional, List
from enum import Enum


class Tile(Enum):
    BLUE = "blue"
    YELLOW = "yellow"
    RED = "red"
    BLACK = "black"
    SNOW = "snow"


WallTiles = List[List[Optional[Tile]]]
