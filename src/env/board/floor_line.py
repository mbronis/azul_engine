"""Represents floor line"""
from src.env.lines import SingleTileLine, MultiTileLine


class FloorLine:
    def __init__(self, size: int = 7) -> None:
        self.tiles = MultiTileLine()
        self.has_1p_token: bool = False
        self.size = size

    def add_broken_tiles(self, broken_tiles: SingleTileLine) -> None:
        self.tiles.extend(broken_tiles)

    def add_1p_token(self) -> None:
        self.has_1p_token = True

    def reset(self) -> None:
        self.tiles = MultiTileLine()
        self.has_1p_token = False

    @property
    def broken_tiles_count(self) -> int:
        return self.tiles.total_filled + int(self.has_1p_token)

    def get_state(self) -> dict:
        return {
            "size": self.size,
            "tiles": self.tiles.get_state(),
            "has_1p_token": self.has_1p_token,
        }
