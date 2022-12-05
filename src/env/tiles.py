"""Represents game tiles"""
from enum import Enum, auto
from dataclasses import dataclass


class Tile(Enum):
    BLUE = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()
    SNOW = auto()


@dataclass
class TilesLine:
    tile: Tile
    size: int
