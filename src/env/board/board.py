"""Represents player's board"""
from typing import Optional, List

from src.env.tiles import Tile, SingleTileLine
from src.env.board.wall import Wall
from src.env.board.pattern_lines import PatternLines
from src.env.board.floor_line import FloorLine
from src.env.actions import AddWallTile
from src.env.states.wall import WallState
from src.env.scoring import Scorer


class Board:
    def __init__(self, wall: Wall) -> None:
        self.score: int = 0
        self.wall = wall
        self.pattern_lines = PatternLines(self.get_size())
        self.floor_line = FloorLine()

    # ------------------
    # -- Info
    # ------------------
    def get_size(self) -> int:
        return self.wall.size

    # ------------------
    # -- Actions Space
    # ------------------
    def can_fill_pattern_line(self, row: int, l: SingleTileLine) -> bool:
        if not self.pattern_lines.can_add(row, l):
            return False
        if not self.wall.can_add_tile_in_row(row, l.tile):
            return False
        return True

    def can_tile_wall(self, row: int, col: int, t: Tile) -> bool:
        return self.wall.can_add_tile(row, col, t)

    # ------------------
    # -- Actions
    # ------------------
    def fill_pattern_line(self, row: int, l: SingleTileLine):
        """Fills pattern line and adds surplus to floor."""
        surplus = self.pattern_lines.fill(row, l)
        self.floor_line.add_broken_tiles(surplus)

    def add_wall_tile(self, a: AddWallTile):
        s: WallState = self.wall.get_state()
        score = Scorer.score_add_wall_tile(s, a)
        self.update_score(score)
        self.add_wall_tile(a)

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

    def finalize_round(self) -> bool:
        flushed_tiles: List[Optional[Tile]] = self.pattern_lines.flush()

    # ------------------
    # -- Mechanics
    # ------------------
    def update_score(self, value: int) -> None:
        self.score = max(0, self.score + value)
