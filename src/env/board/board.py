"""Represents player's board"""
from dataclasses import dataclass


@dataclass
class Board:
    def __init__(self) -> None:
        self.points: int = 0
        self.wall = self._init_wall()
        self.pattern_lines = self._init_pattern_lines()
        self.floor_line = self._init_floor_line()

    def update_points(self, value: int) -> None:
        # TODO: all rules to a single module
        self.points = max(0, self.points + value)

    def _init_wall(self):
        pass

    def _init_pattern_lines(self):
        pass

    def _init_floor_line(self):
        pass
