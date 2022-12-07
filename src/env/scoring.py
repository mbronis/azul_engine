from src.env.actions import AddWallTile
from src.env.states.wall_state import WallState

# TODO: make abc
class Scorer:
    # TODO: refactor to abstract attributes
    BASE_NEIGHBOR_SCORE = 1
    FILLED_ROW_SCORE = 2
    FILLED_COL_SCORE = 7
    FILLED_COLOR_SCORE = 10

    @classmethod
    def score_add_wall_tile(cls, s: WallState, a: AddWallTile) -> int:
        size = s.size
        neighbors_row = s.count_neighbors_row(a.row, a.col)
        neighbors_col = s.count_neighbors_col(a.row, a.col)
        tile_count = s.get_tile_count(a.tile)

        score = 0
        score += cls._score_num_neighbor(neighbors_row, neighbors_col)
        score += cls._score_filled_row(neighbors_row, size)
        score += cls._score_filled_col(neighbors_row, size)
        score += cls._score_filled_color(tile_count, size)
        return score

    @classmethod
    def _score_num_neighbor(cls, neighbors_row: int, neighbors_col: int) -> int:
        return cls.BASE_NEIGHBOR_SCORE + neighbors_row + neighbors_col

    @classmethod
    def _score_filled_row(cls, neighbors_row: int, size: int) -> int:
        if neighbors_row == size - 1:
            return cls.FILLED_ROW_SCORE

    @classmethod
    def _score_filled_col(cls, neighbors_row: int, size: int) -> int:
        if neighbors_row == size - 1:
            return cls.FILLED_COL_SCORE

    @classmethod
    def _score_filled_color(cls, tile_count: int, size: int) -> int:
        if tile_count == size - 1:
            return cls.FILLED_COLOR_SCORE

    @classmethod
    def _score_floor_line_flush(cls, floor_len: int) -> int:
        # TODO: implement
        return 0