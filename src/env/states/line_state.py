from dataclasses import dataclass


from src.env.tiles import Tile


@dataclass
class SingleTileLineState:
    filled: int
    size: int
    tile: Tile


# @dataclass
# class MultiTileLineState:
#     filled: int
#     size: int
#     tile: Tile
