from dataclasses import dataclass
from typing import List

from src.env.tiles import Tile
from src.env.lines import SingleTileLine


@dataclass
class AddWallTileAction:
    row: int
    col: int
    tile: Tile


@dataclass
class AddAllWallTilesAction:
    """Adds tiles from all pattern lines to wall"""

    line_actions: List[AddWallTileAction]


@dataclass
class FillPatternLineAction:
    row: int
    line: SingleTileLine
