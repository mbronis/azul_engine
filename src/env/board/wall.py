from collections import defaultdict

from src.env.tiles import Tile, WallTiles
from src.env.scoring import Scorer
from src.env.states.wall import WallState


class Wall:
    def __init__(self, size: int, filled: WallTiles = None, expected: WallTiles = None):
        self.size = size
        self._filled = filled or [[None for _ in range(self.size)] for _ in range(self.size)]
        self._expected = expected or [[None for _ in range(self.size)] for _ in range(self.size)]
        self._tiles_count = defaultdict(int)

    # ------------------
    # -- Info
    # ------------------

    def _is_filled(self, row: int, col: int) -> bool:
        return self._filled[row][col] is not None

    # TODO: refactor unittests and remove
    def _count_neighbors_row(self, row: int, col: int) -> int:
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

    # TODO: refactor unittests and remove
    def _count_neighbors_col(self, row: int, col: int) -> int:
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

    # TODO: refactor unittests and remove
    def _count_neighbors(self, row: int, col: int) -> int:
        return self._count_neighbors_row(row, col) + self._count_neighbors_col(row, col)

    # ------------------
    # -- Actions Space
    # ------------------
    def get_state(self) -> WallState:
        return WallState(size=self.size, filled=self._filled, tiles_count=self._tiles_count)

    def _is_expected(self, row: int, col: int, t: Tile) -> bool:
        return (self._expected[row][col] or t) == t

    def _get_row_fills(self, i: int) -> set[Tile]:
        return set(t for t in self._filled[i] if t)

    def _get_col_fills(self, col: int) -> set[Tile]:
        return set(self._filled[r][col] for r in range(self.size) if self._filled[r][col])

    def can_add_tile(self, row: int, col: int, t: Tile) -> bool:
        if self._is_filled(row, col):
            return False
        if not self._is_expected(row, col, t):
            return False
        if t in self._get_row_fills(row):
            return False
        if t in self._get_col_fills(col):
            return False
        return True

    def can_add_tile_in_row(self, row: int, t: Tile) -> bool:
        for col in range(self.size):
            if self.can_add_tile(row, col, t):
                return True
        return False

    # ------------------
    # -- Actions
    # ------------------

    def add_tile(self, row: int, col: int, t: Tile) -> None:
        """Adds tile to wall."""
        self._filled[row][col] = t

    # ------------------
    # -- Mechanics
    # ------------------

    # def _score(self, row: int, col: int, t: Tile) -> int:
    #     """Returns score for adding a tile to wall."""
    #     score = 0
    #     score += self.BASE_NEIGHBOR + self._count_neighbors(row, col)
    #     if self._count_neighbors_row(row, col) + 1 == self.size:
    #         score += self.FILLED_ROW
