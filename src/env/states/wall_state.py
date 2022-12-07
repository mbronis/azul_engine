from dataclasses import dataclass
from collections import defaultdict

from src.env.tiles import Tile, WallTiles


@dataclass
class WallState:
    size: int
    filled: WallTiles
    tiles_count: defaultdict(int)

    def _is_filled(self, row: int, col: int) -> bool:
        return self.filled[row][col] is not None

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

    def get_tile_count(self, tile: Tile) -> int:
        return self.tiles_count[tile]
