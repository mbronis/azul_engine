from enum import Enum, auto

from src.env.tiles import Tile
from src.env.board.wall import Wall


class FreeWall(Wall):
    def __init__(self):
        super().__init__(size=5)


class FixedWall(Wall):
    def __init__(self):
        super().__init__(
            size=5,
            expected=[
                [Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW],
                [Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED, Tile.BLACK],
                [Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW, Tile.RED],
                [Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE, Tile.YELLOW],
                [Tile.YELLOW, Tile.RED, Tile.BLACK, Tile.SNOW, Tile.BLUE],
            ],
        )


def get_wall(wall_name: str) -> Wall:
    walls = {
        "free": FreeWall(),
        "fixed": FixedWall(),
    }
    return walls[wall_name]
