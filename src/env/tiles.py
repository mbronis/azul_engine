"""Represents game tiles and tiles collections."""
from __future__ import annotations
from typing import Optional
from copy import copy
from enum import Enum, auto


class Tile(Enum):
    BLUE = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()
    SNOW = auto()


class SingleTileLine:
    def __init__(self, filled: int = 0, size: int = None, tile: Tile = None) -> None:
        if size and (size < filled):
            msg = f"Cant initialize {self.__class__.__name__} with size < filled: "
            msg += f"{size} < {filled}."
            raise AttributeError(msg)
        if filled < 0:
            msg = f"Cant initialize {self.__class__.__name__} with filled < 0: "
            msg += f"{filled} < 0."
            raise AttributeError(msg)
        self.filled = filled
        self.size = size or max(1, filled)
        self.tile = tile

    def can_add(self, l: SingleTileLine) -> bool:
        if self.tile and (self.tile != l.tile):
            return False
        return True

    def fill(self, l: SingleTileLine) -> int:
        """Increases filled up to size and returns value of surplus."""
        if not self.can_add(l):
            msg = f"Tiles mismatch on fill - tied to fill {self.tile} with {l.tile}."
            raise AttributeError(msg)
        surplus = max(0, l.filled - (self.size - self.filled))
        self.tile = l.tile
        self.filled += l.filled - surplus
        return surplus

    def extend(self, l: SingleTileLine) -> None:
        """Increases filled and size if needed."""
        if not self.can_add(l):
            msg = f"Tiles mismatch on extend - tied to extend {self.tile} with {l.tile}."
            raise AttributeError(msg)
        self.tile = l.tile
        self.filled += l.filled
        self.size = max(self.size, self.filled)

    def flush(self) -> Optional[Tile]:
        """Clears filled if full and returns Tile"""
        tile = None
        if self.filled == self.size:
            tile = copy(self.tile)
            self.filled = 0
            self.tile = None

        return tile


# class MultiTileLine:
#     def __init__(self, size: int, filled: Optional[List[Optional[Tile]]] = None):
#         self.size = size
#         self._filled: List[Optional[Tile]] = filled or [None for _ in range(self.size)]

#     @property
#     def len(self) -> int:
#         return len(t for t in self._filled if t)

#     def _reset(self):
#         self._filled = [None for _ in range(self.size)]

#     def flush(self) -> int:
#         """Resets and returns len before reset."""
#         l = self.len()
#         self._reset()
#         return l

#     def append_single_tile_line(self, l: SingleTileLine) -> SingleTileLine:
#         """Fills self._filled and returns remainder."""
#         pass

#     def append_multi_tile_line(self, l: MultiTileLine) -> MultiTileLine:
#         """Fills self._filled and returns remainder."""
#         pass
