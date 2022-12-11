"""Represents floor line"""
from src.env.lines import SingleTileLine, MultiTileLine


class FloorLine:
    def __init__(self) -> None:
        self.tiles = MultiTileLine()
        self.has_first_player_token: bool = False

    def add_broken_tiles(self, broken_tiles: SingleTileLine) -> None:
        self.tiles.extend(broken_tiles)

    def add_first_player_token(self) -> None:
        self.has_first_player_token = True

    def reset(self) -> None:
        self.tiles = MultiTileLine()
        self.has_first_player_token = False

    @property
    def broken_tiles_count(self) -> int:
        return self.tiles.total_filled + int(self.has_first_player_token)

    def get_state(self) -> dict:
        return self.tiles.get_state()
