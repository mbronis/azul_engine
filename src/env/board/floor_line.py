"""Represents floor line"""


class FloorLine:
    def __init__(self, size: int = 7) -> None:
        self.size = size
        self.filled: int = 0
        self.has_first_player_token: bool = False

    def add_tiles(self, value: int) -> None:
        self.filled += value
        self.filled = min(self.size, self.filled)

    def add_first_player_token(self) -> None:
        self.has_first_player_token = True

    def reset(self) -> None:
        self.filled = 0
        self.has_first_player_token = False
