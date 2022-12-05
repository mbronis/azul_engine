from typing import List, Optional

from src.env.tiles import Tile


class Wall:
    SIZE = 5

    def __init__(self) -> None:
        self._filled: List[List[Optional[Tile]]] = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._expected: List[List[Optional[Tile]]] = [[None for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def is_filled(self, row: int, col: int) -> bool:
        return self._filled[row][col] is not None

    def is_expected(self, row: int, col: int, t: Tile) -> bool:
        return (self._expected[row][col] or t) == t

    def get_row_fills(self, i: int) -> set[Tile]:
        return set(t for t in self._filled[i] if t)

    def get_col_fills(self, col: int) -> set[Tile]:
        return set(self._filled[r][col] for r in range(self.SIZE) if self._filled[r][col])


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
