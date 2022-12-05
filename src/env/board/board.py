"""Represents player's board"""
from typing import Optional, List

from src.env.tiles import Tile, SingleTileLine
from src.env.board.wall import Wall
from src.env.board.pattern_lines import PatternLines
from src.env.board.floor_line import FloorLine


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
    # -- Actions
    # ------------------
    def can_add(self, row: int, l: SingleTileLine) -> bool:
        if not self.pattern_lines.can_add(row, l):
            return False
        if not self.wall.can_add_to_row(row, l.tile):
            return False
        return True

    # ------------------
    # -- Mechanics
    # ------------------
    def add_score(self, value: int) -> None:
        self.score = max(0, self.score + value)

    def finalize_round(self) -> bool:
        flushed_tiles: List[Optional[Tile]] = self.pattern_lines.flush()
