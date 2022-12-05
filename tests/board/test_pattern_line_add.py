import pytest

from src.env.tiles import Tile, TilesLine
from src.env.board.pattern_lines import PatternLine

SIZE = 5
TILE = Tile.BLACK
OTHER_TILE = Tile.SNOW

scenarios = [
    {
        "name": "can add to empty line",
        "pattern_filled": 0,
        "pattern_tile": None,
        "added_size": 1,
        "added_tile": TILE,
        "expected": True,
    },
    {
        "name": "can add with more than size",
        "pattern_tile": TILE,
        "pattern_filled": 0,
        "added_tile": TILE,
        "added_size": 6,
        "expected": True,
    },
    {
        "name": "can't add with tiles mismatch",
        "pattern_tile": TILE,
        "pattern_filled": 0,
        "added_tile": OTHER_TILE,
        "added_size": 1,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_pattern_line_can_add(scen):
    pattern_line = PatternLine(SIZE, scen["pattern_filled"], scen["pattern_tile"])
    added_line = TilesLine(scen["added_tile"], scen["added_size"])
    actual = pattern_line.can_add_tiles_line(added_line)
    expected = scen["expected"]
    assert actual == expected
