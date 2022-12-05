from typing import List, Optional

from src.env.tiles import Tile


class Wall:
    SIZE = 5

    def __init__(self) -> None:
        self._filled: List[List[Optional[Tile]]] = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._expected: List[List[Optional[Tile]]] = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def _is_filled(self, row: int, col: int) -> bool:
        return self._filled[row][col] is not None

    def _is_expected(self, row: int, col: int, t: Tile) -> bool:
        return (self._expected[row][col] or t) == t

    def _get_row_fills(self, i: int) -> set[Tile]:
        return set(t for t in self._filled[i] if t)

    def _get_col_fills(self, col: int) -> set[Tile]:
        return set(self._filled[r][col] for r in range(self.SIZE) if self._filled[r][col])

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


class FixedWall(Wall):
    def __init__(self) -> None:
        super().__init__()
        self._expected = [
            [Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW],
            [Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK],
            [Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED],
            [Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW],
            [Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE],
        ]
