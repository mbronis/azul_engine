from typing import List, Optional
from src.env.tiles import Tile

WallTiles = List[List[Optional[Tile]]]


class Wall:
    def __init__(self, size: int, filled: WallTiles = None, expected: WallTiles = None):
        self.size = size
        self._filled = filled or [[None for _ in range(self.size)] for _ in range(self.size)]
        self._expected = expected or [[None for _ in range(self.size)] for _ in range(self.size)]

    def can_fill(self, row: int, col: int, t: Tile) -> bool:
        if self._is_filled(row, col):
            return False
        if not self._is_expected(row, col, t):
            return False
        if t in self._get_row_fills(row):
            return False
        if t in self._get_col_fills(col):
            return False
        return True

    def _is_filled(self, row: int, col: int) -> bool:
        return self._filled[row][col] is not None

    def _is_expected(self, row: int, col: int, t: Tile) -> bool:
        return (self._expected[row][col] or t) == t

    def _get_row_fills(self, i: int) -> set[Tile]:
        return set(t for t in self._filled[i] if t)

    def _get_col_fills(self, col: int) -> set[Tile]:
        return set(self._filled[r][col] for r in range(self.size) if self._filled[r][col])

    def count_neighbors_row(self, row: int, col: int) -> int:
        neighbors = 0
        for i in range(self.size - 1 - col):
            if not self._is_filled(row, col + i + 1):
                break
            neighbors += 1
        for i in range(col):
            if not self._is_filled(row, col - i - 1):
                break
            neighbors += 1
        return neighbors

    def count_neighbors_col(self, row: int, col: int) -> int:
        neighbors = 0
        for i in range(self.size - 1 - row):
            print(f"{row + i + 1, col}: {self._is_filled(row + i + 1, col)}")
            if not self._is_filled(row + i + 1, col):
                break
            neighbors += 1
        for i in range(row):
            if not self._is_filled(row - i - 1, col):
                break
            neighbors += 1
        return neighbors

    def count_neighbors(self, row: int, col: int) -> int:
        return self.count_neighbors_row(row, col) + self.count_neighbors_col(row, col)


class FreeWall(Wall):
    def __init__(self):
        super().__init__(size=5)


class FixedWall(Wall):
    def __init__(self):
        super().__init__(
            size=5,
            expected=[
                [Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW],
                [Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK],
                [Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED],
                [Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW],
                [Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE],
            ],
        )
