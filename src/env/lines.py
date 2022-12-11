"""Represents basic Tiles container classes"""
from __future__ import annotations

import random
from typing import Optional, List
from copy import copy, deepcopy

from src.env.tiles import Tile


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

    def fill(self, l: SingleTileLine) -> SingleTileLine:
        """Increases filled up to size and returns value of surplus."""
        if not self.can_add_tile(l.tile):
            msg = f"Tiles mismatch on fill - tied to fill {self.tile} with {l.tile}."
            raise AttributeError(msg)
        surplus = max(0, l.filled - (self.size - self.filled))
        self.tile = self.tile or l.tile
        self.filled += l.filled - surplus

        return SingleTileLine(filled=surplus, tile=l.tile)

    def fill_max(self) -> None:
        """Fills up to the size."""
        self.filled = self.size

    def reset(self, reset_tile: bool = False) -> None:
        self.filled = 0
        if reset_tile:
            self.tile = None

    def extend(self, l: SingleTileLine) -> None:
        """Increases filled and size if needed."""
        if not self.can_add_tile(l.tile):
            msg = f"Tiles mismatch on extend - tied to extend {self.tile} with {l.tile}."
            raise AttributeError(msg)
        self.tile = self.tile or l.tile
        self.filled += l.filled
        self.size = max(self.filled, self.size, l.size)

    def add_one(self, t: Tile) -> None:
        """Extends by one tile."""
        if not self.can_add_tile(t):
            msg = f"Tiles mismatch on add_one: tied to add {t} to {self.tile}."
            raise AttributeError(msg)
        self.tile = self.tile or t
        self.filled += 1
        self.size = max(self.size, self.filled)

    def get_one(self) -> Tile:
        """Returns single tile."""
        if not self.filled:
            raise RuntimeError("Tried to get_one from empty SingleTileLine")
        self.filled -= 1
        return self.tile

    def flush(self) -> Optional[Tile]:
        """Clears filled if full and returns Tile"""
        tile = None
        if self.filled == self.size:
            tile = copy(self.tile)
            self.filled = 0
            self.tile = None

        return tile

    def get_state(self) -> dict:
        return {self.tile.value if self.tile else None: self.filled}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"


class MultiTileLine:
    def __init__(self):
        self.tiles: dict[Tile, SingleTileLine] = {tile: SingleTileLine(tile=tile) for tile in Tile}

    @classmethod
    def from_tiles(cls, tiles: List[Tile]) -> MultiTileLine:
        multi_line = MultiTileLine()
        for t in tiles:
            multi_line.tiles[t].add_one(t)
        return multi_line

    def extend(self, l: SingleTileLine):
        """Extend tiles"""
        self.tiles[l.tile].extend(l)

    def merge(self, m: MultiTileLine):
        """Combine tiles of other MultiLineLine"""
        for t, l in m.tiles.items():
            self.tiles[t].extend(l)

    def get_all(self, t: Tile) -> SingleTileLine:
        """Returns all tiles of selected type."""
        line = deepcopy(self.tiles[t])
        self.tiles[t].filled = 0
        return line

    def get_one(self, t: Tile) -> Tile:
        return self.tiles[t].get_one()

    def _get_one_random(self) -> Tile:
        """Returns single tile selected at random from filled tiles."""
        weights = [self.tiles[t].filled for t in Tile]
        tile = random.choices(list(Tile), weights=weights)[0]
        return self.get_one(tile)

    def get_random(self, n: int) -> MultiTileLine:
        """Selects n tiles at random from tiles."""
        n = min(n, self.total_filled)
        selected = []
        while len(selected) < n:
            tile = self._get_one_random()
            selected.append(tile)
        return MultiTileLine.from_tiles(selected)

    def fill_max(self) -> None:
        """Fills all tiles up to the size."""
        for tile_line in self.tiles.values():
            tile_line.fill_max()

    def reset(self) -> None:
        for tile_line in self.tiles.values():
            tile_line.reset()

    @property
    def total_filled(self) -> int:
        """Returns total number of filled tiles"""
        return sum(t.filled for t in self.tiles.values())

    def get_state(self) -> dict:
        return {k: v for d in self.tiles.values() for k, v in d.get_state().items()}

    def __repr__(self) -> str:
        r = f"{self.__class__.__name__}("
        for l in self.tiles.values():
            r += "\n\t" + str(l)
        r += ")"
        return r