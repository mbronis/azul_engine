from typing import Optional, List


from src.env.tiles import Tile
from src.env.lines import SingleTileLine


class PatternLines:
    def __init__(self, size: int) -> None:
        self._lines = [SingleTileLine(size=row_len + 1) for row_len in range(size)]

    def flush(self) -> List[Optional[Tile]]:
        return [line.flush() for line in self._lines]

    def can_add_tile(self, row: int, t: Tile) -> bool:
        return self._lines[row].can_add_tile(t)

    def fill(self, row: int, l: SingleTileLine) -> SingleTileLine:
        return self._lines[row].fill(l)

    def reset(self) -> None:
        for line in self._lines:
            line.reset(reset_tile=True)

    def get_state(self) -> dict:
        return [l.get_state() for l in self._lines]
