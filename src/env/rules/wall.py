from re import I
from src.env.tiles import Tile
from src.env.board.wall import Wall


def can_fill(w: Wall, row: int, col: int, t: Tile) -> bool:
    if w.is_filled(row, col):
        return False
    if not w.is_expected(row, col, t):
        return False
    if t in w.get_row_fills(row):
        return False
    if t in w.get_col_fills(col):
        return False
    return True
