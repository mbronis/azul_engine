"""Represents floor line"""

SIZE = 7


class FloorLine:
    def __init__(self) -> None:
        self.broken_tiles_count: int = 0
        self.has_first_player_token: bool = False

    def add_broken_tiles(self, value: int) -> None:
        self.broken_tiles_count += value
        self.broken_tiles_count = min(SIZE, self.broken_tiles_count)

    def add_first_player_token(self) -> None:
        self.has_first_player_token = True

    def reset(self) -> None:
        self.broken_tiles_count = 0
        self.has_first_player_token = False
