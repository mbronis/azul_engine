"""Represents game tiles and tiles collections."""
from __future__ import annotations
from typing import Optional, List
from copy import copy
from enum import Enum, auto
from collections import defaultdict


class Tile(Enum):
    BLUE = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()
    SNOW = auto()


WallTiles = List[List[Optional[Tile]]]


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

    def can_add_tile(self, tile: Tile) -> bool:
        if self.tile and (self.tile != tile):
            return False
        return True

    def can_add_line(self, l: SingleTileLine) -> bool:
        return self.can_add_tile(l.tile)

    def fill(self, l: SingleTileLine) -> int:
        """Increases filled up to size and returns value of surplus."""
        if not self.can_add_line(l):
            msg = f"Tiles mismatch on fill - tied to fill {self.tile} with {l.tile}."
            raise AttributeError(msg)
        surplus = max(0, l.filled - (self.size - self.filled))
        self.tile = l.tile
        self.filled += l.filled - surplus
        return surplus

    def extend(self, l: SingleTileLine) -> None:
        """Increases filled and size if needed."""
        if not self.can_add_line(l):
            msg = f"Tiles mismatch on extend - tied to extend {self.tile} with {l.tile}."
            raise AttributeError(msg)
        self.tile = self.tile or l.tile
        self.filled += l.filled
        self.size = max(self.size, self.filled)

    def add_one(self, t: Tile) -> None:
        """Extends by one tile"""
        if not self.can_add_tile(t):
            msg = f"Tiles mismatch on add_one: tied to add {t} to {self.tile}."
            raise AttributeError(msg)
        self.tile = self.tile or t
        self.filled += 1
        self.size = max(self.size, self.filled)

    def flush(self) -> Optional[Tile]:
        """Clears filled if full and returns Tile"""
        tile = None
        if self.filled == self.size:
            tile = copy(self.tile)
            self.filled = 0
            self.tile = None

        return tile

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class MultiTileLine:
    def __init__(self, tiles: List[Tile] = None):
        self.tiles = defaultdict(lambda: SingleTileLine())
        if not tiles:
            return

        for t in tiles:
            self.tiles[t].add_one(t)

    def __repr__(self) -> str:
        r = f"{self.__class__.__name__}("
        for l in self.tiles.values():
            r += "\n\t" + str(l)
        r += ")"
        return r

    def extend(self, l: SingleTileLine):
        """Extend tiles"""
        self.tiles[l.tile].extend(l)

    def merge(self, m: MultiTileLine):
        """Combine tiles of other MultiLineLine"""
        for t, l in m.tiles.items():
            self.tiles[t].extend(l)

    def get(self, t: Tile) -> SingleTileLine:
        """Returns all tiles of selected type."""
        if t not in self.tiles:
            return SingleTileLine(tile=t)
        return self.tiles.pop(t)

    @property
    def total_size(self) -> int:
        """Returns total number of filled tiles"""
        return sum(t.filled for t in self.tiles.values())
