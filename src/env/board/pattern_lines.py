from typing import Optional, List


from src.env.tiles import Tile, SingleTileLine


class PatternLines:
    def __init__(self, size: int = 5) -> None:
        self._lines = [SingleTileLine(size=row_len) for row_len in range(size)]

    def flush(self) -> List[Optional[Tile]]:
        return [line.flush() for line in self._lines]

    def can_add(self, row: int, l: SingleTileLine) -> bool:
        return self._lines[row].can_add_line(l)

    def fill(self, row: int, l: SingleTileLine) -> int:
        return self._lines[row].fill(l)
