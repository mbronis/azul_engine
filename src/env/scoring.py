from src.env.board.rules import AzulRules
from src.env.actions import AddWallTileAction
from src.env.states.wall_state import WallState


class Scorer:
    def __init__(self, rules: AzulRules):
        self.base_wall_fill_points = rules.points_self
        self.filled_row_points = rules.points_row_fill
        self.filled_col_points = rules.points_col_fill
        self.filled_color_points = rules.points_color_fill
        self.floor_penalties = rules.floor_penalties

    def score_add_wall_tile(self, s: WallState, a: AddWallTileAction) -> int:
        neighbors_row = s.count_neighbors_row(a.row, a.col)
        neighbors_col = s.count_neighbors_col(a.row, a.col)
        tile_count = s.get_tile_count(a.tile)

        score = 0
        score += self._score_num_neighbor(neighbors_row, neighbors_col)
        score += self._score_filled_row(neighbors_row, s.size)
        score += self._score_filled_col(neighbors_row, s.size)
        score += self._score_filled_color(tile_count, s.size)
        return score

    def score_floor_line_penalty(self, floor_len: int) -> int:
        return sum(self.floor_penalties[:floor_len])

    def _score_num_neighbor(self, neighbors_row: int, neighbors_col: int) -> int:
        return self.base_wall_fill_points + neighbors_row + neighbors_col

    def _score_filled_row(self, neighbors_row: int, size: int) -> int:
        if neighbors_row == size - 1:
            return self.filled_row_points

    def _score_filled_col(self, neighbors_row: int, size: int) -> int:
        if neighbors_row == size - 1:
            return self.filled_col_points

    def _score_filled_color(self, tile_count: int, size: int) -> int:
        if tile_count == size - 1:
            return self.filled_color_points
