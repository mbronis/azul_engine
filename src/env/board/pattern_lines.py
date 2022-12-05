from typing import Optional, List
from dataclasses import dataclass


from src.env.tiles import Tile, TilesLine


@dataclass
class PatternLine:
    size: int
    filled: int = 0
    tile: Optional[Tile] = None

    def reset(self):
        self.filled = 0
        self.tile = None

    def flush(self) -> Optional[Tile]:
        tile = None
        if self.filled == self.size:
            tile = self.tile
            self.reset()

        return tile

    def can_add_tiles_line(self, l: TilesLine) -> bool:
        if (self.tile or l.tile) != l.tile:
            return False
        return True

    def add_tiles_line(self, l: TilesLine) -> TilesLine:
        """Fills Pattern Line and returns remaining tiles."""
        remainder = TilesLine(
            tile=l.tile,
            size=max(0, l.size - (self.size - self.filled)),
        )
        self.tile = l.tile
        self.filled += l.size - remainder.size

        return remainder


class PatternLines:
    def __init__(self, size: int = 5) -> None:
        self._lines = [PatternLine(row) for row in range(size)]

    def flush(self) -> List[Optional[Tile]]:
        return [l.flush() for l in self._lines]

    def get_row_tile(self, row: int) -> Tile:
        return self._lines[row].tile