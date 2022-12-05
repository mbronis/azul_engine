import pytest

from src.env.tiles import Tile, TilesLine
from src.env.board.pattern_lines import PatternLine

SIZE = 5
TILE = Tile.BLACK
OTHER_TILE = Tile.SNOW

scenarios_can_add = [
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


@pytest.mark.parametrize("scen", scenarios_can_add, ids=(scen["name"] for scen in scenarios_can_add))
def test_pattern_line_can_add(scen):
    pattern_line = PatternLine(SIZE, scen["pattern_filled"], scen["pattern_tile"])
    added_line = TilesLine(scen["added_tile"], scen["added_size"])
    actual = pattern_line.can_add_tiles_line(added_line)
    expected = scen["expected"]
    assert actual == expected


scenarios_add = [
    {
        "name": "add to empty pattern line",
        "pattern_filled": 0,
        "pattern_tile": None,
        "added_size": 1,
        "added_tile": TILE,
        "expected": {
            "pattern_filled": 1,
            "pattern_tile": TILE,
            "remainder_size": 0,
            "remainder_tile": TILE,
        },
    },
    {
        "name": "add long tiles line",
        "pattern_filled": 0,
        "pattern_tile": TILE,
        "added_size": 6,
        "added_tile": TILE,
        "expected": {
            "pattern_filled": SIZE,
            "pattern_tile": TILE,
            "remainder_size": 1,
            "remainder_tile": TILE,
        },
    },
    {
        "name": "add to full pattern line",
        "pattern_filled": SIZE,
        "pattern_tile": TILE,
        "added_size": 1,
        "added_tile": TILE,
        "expected": {
            "pattern_filled": SIZE,
            "pattern_tile": TILE,
            "remainder_size": 1,
            "remainder_tile": TILE,
        },
    },
]


@pytest.mark.parametrize("scen", scenarios_add, ids=(scen["name"] for scen in scenarios_add))
def test_pattern_line_add_tiles_line(scen):
    pattern_line = PatternLine(SIZE, scen["pattern_filled"], scen["pattern_tile"])
    added_line = TilesLine(scen["added_tile"], scen["added_size"])
    remainder_line = pattern_line.add_tiles_line(added_line)
    actual = {
        "pattern_filled": pattern_line.filled,
        "pattern_tile": pattern_line.tile,
        "remainder_size": remainder_line.size,
        "remainder_tile": remainder_line.tile,
    }
    assert actual == scen["expected"]


def test_pattern_line_add_tiles_line_with_mismatch_tile():
    pattern_line = PatternLine(SIZE, 0, TILE)
    added_line = TilesLine(OTHER_TILE, 1)
    with pytest.raises(AttributeError):
        pattern_line.add_tiles_line(added_line)
