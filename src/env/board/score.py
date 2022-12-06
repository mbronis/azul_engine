from src.env.tiles import Tile
from src.env.board.wall import Wall

BASE_NEIGHBOR = 1
FILLED_ROW = 2
FILLED_COL = 7
FILLED_COLOR = 10


def num_neighbor(wall: Wall, tile: Tile, row: int, col: int) -> int:
    return BASE_NEIGHBOR + wall._count_neighbors(row, col)


def filled_row(wall: Wall, tile: Tile, row: int, col: int) -> int:
    if wall._count_neighbors_row(row, col) + 1 == wall.size:
        return FILLED_ROW


def filled_column(wall: Wall, tile: Tile, row: int, col: int) -> int:
    if wall._count_neighbors_col(row, col) + 1 == wall.size:
        return FILLED_COL


def filled_color(wall: Wall, tile: Tile, row: int, col: int) -> int:
    # TODO: implement
    return 0


def floor_line_penalty(floor_len: int) -> int:
    # TODO: implement
    return 0
