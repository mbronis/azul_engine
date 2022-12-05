import pytest

from src.env.tiles import Tile
from src.env.board.pattern_lines import PatternLine

SIZE = 5
TILE = Tile.BLACK

scenarios = [
    {"name": "flush fully filled", "filled": 5, "expected": TILE},
    {"name": "flush partially filled", "filled": 4, "expected": None},
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_pattern_line_flush(scen):
    pattern_line = PatternLine(SIZE, scen["filled"], TILE)
    actual = pattern_line.flush()
    expected = scen["expected"]
    assert actual == expected


def test_pattern_line_flush_empty():
    pattern_line = PatternLine(SIZE)
    actual = pattern_line.flush()
    expected = None
    assert actual == expected
