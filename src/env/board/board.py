"""Represents player's board"""
from typing import Optional, List

from src.env.tiles import Tile
from src.env.lines import SingleTileLine
from src.env.board.wall import Wall
from src.env.board.pattern_lines import PatternLines
from src.env.board.floor_line import FloorLine
from src.env.states.wall_state import WallState
from src.env.scoring import Scorer
from src.env.actions import AddWallTileAction, FillPatternLineAction


class Board:
    def __init__(self, wall: Wall, floor_size: int, player_name: str) -> None:
        self.score: int = None
        self.player_name = player_name
        self.wall = wall
        self.pattern_lines = PatternLines(self.wall.size)
        self.floor_line = FloorLine(floor_size)

    # ------------------
    # -- Info
    # ------------------
    def get_state(self) -> dict:
        return {
            "score": self.score,
            "player_name": self.player_name,
            "wall": self.wall.get_state_dict(),
            "pattern_lines": self.pattern_lines.get_state(),
            "floor_line": self.floor_line.get_state(),
        }

    def add_1p_token(self) -> None:
        self.floor_line.add_1p_token()

    # ------------------
    # -- Actions Space
    # ------------------
    def can_fill_pattern_line(self, t: Tile, row: int = None) -> bool:
        if row is None:
            return True
        if not self.pattern_lines.can_add_tile(row, t):
            return False
        if not self.wall.can_add_tile_in_row(row, t):
            return False
        return True

    def can_tile_wall(self, row: int, col: int, t: Tile) -> bool:
        return self.wall.can_add_tile(row, col, t)

    # ------------------
    # -- Actions
    # ------------------
    # TODO: add tests
    def fill_pattern_line(self, l: SingleTileLine, row: int = None):
        """Fills pattern line and adds surplus to floor.
        If row not provided fills floor with whole line.
        """
        if row is not None:
            l = self.pattern_lines.fill(row, l)
        self.floor_line.add_broken_tiles(l)

    # TODO: add tests
    def add_wall_tile(self, a: AddWallTileAction):
        r, c, t = a.row, a.col, a.tile
        if not self.can_tile_wall(r, c, t):
            raise AttributeError("cannot add wall tile")

        self.wall.add_tile(r, c, t)
        s: WallState = self.wall.get_state()
        score = Scorer.score_add_wall_tile(s, a)
        self.update_score(score)

    def finalize_round(self) -> bool:
        flushed_tiles: List[Optional[Tile]] = self.pattern_lines.flush()

    # def tile_wall(self, columns: List[int]) -> int:
    #     """
    #     Moves tiles from completed pattern lines and add them to the wall.

    #     Arguments
    #     ---------
    #         columns : int
    #             indicate wall columns to fill for each pattern line

    #     Returns
    #     -------
    #         int : scores
    #     """
    #     flushed_tiles: List[Optional[Tile]] = self.pattern_lines.flush()
    #     for row, column, tile in enumerate(zip(columns, flushed_tiles)):
    #         if tile:

    # ------------------
    # -- Mechanics
    # ------------------
    def update_score(self, value: int) -> None:
        self.score = max(0, self.score + value)

    def reset(self) -> None:
        self.score = 0
        self.wall.reset()
        self.pattern_lines.reset()
        self.floor_line.reset()
