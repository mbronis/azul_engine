import pytest

from src.env.tiles import Tile
from src.env.lines import SingleTileLine

TILE = Tile.BLACK
OTHER_TILE = Tile.SNOW

scenarios_can_add = [
    {
        "name": "can fill empty line",
        "line_tile": None,
        "other_len": 1,
        "other_tile": TILE,
        "expected": True,
    },
    {
        "name": "can fill with more than size",
        "line_filled": 1,
        "line_size": 5,
        "line_tile": TILE,
        "other_filled": 6,
        "other_tile": TILE,
        "expected": True,
    },
    {
        "name": "can't add with tiles mismatch",
        "line_tile": TILE,
        "other_tile": OTHER_TILE,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios_can_add, ids=(scen["name"] for scen in scenarios_can_add))
def test_can_add(scen):
    line_filled, line_size, line_tile = scen.get("line_filled", 0), scen.get("line_size"), scen.get("line_tile")
    other_filled, other_size, other_tile = scen.get("other_filled", 0), scen.get("other_size"), scen.get("other_tile")

    line = SingleTileLine(line_filled, line_size, line_tile)
    other = SingleTileLine(other_filled, other_size, other_tile)
    actual = line.can_add_line(other)
    expected = scen["expected"]
    assert actual == expected


scenarios_fill = [
    {
        "name": "fill empty line",
        "line_filled": 0,
        "line_tile": None,
        "other_filled": 1,
        "other_tile": TILE,
        "expected": {
            "line_filled": 1,
            "line_tile": TILE,
            "reminder": 0,
        },
    },
    {
        "name": "fill without reminder",
        "line_filled": 1,
        "line_size": 5,
        "line_tile": TILE,
        "other_filled": 1,
        "other_tile": TILE,
        "expected": {
            "line_filled": 2,
            "line_tile": TILE,
            "reminder": 0,
        },
    },
    {
        "name": "fill with reminder",
        "line_filled": 1,
        "line_size": 5,
        "line_tile": TILE,
        "other_filled": 6,
        "other_tile": TILE,
        "expected": {
            "line_filled": 5,
            "line_tile": TILE,
            "reminder": 2,
        },
    },
]


@pytest.mark.parametrize("scen", scenarios_fill, ids=(scen["name"] for scen in scenarios_fill))
def test_fill(scen):
    line_filled, line_size, line_tile = scen.get("line_filled", 0), scen.get("line_size"), scen.get("line_tile")
    other_filled, other_size, other_tile = scen.get("other_filled", 0), scen.get("other_size"), scen.get("other_tile")

    line = SingleTileLine(line_filled, line_size, line_tile)
    other = SingleTileLine(other_filled, other_size, other_tile)
    reminder = line.fill(other)

    actual = {
        "line_filled": line.filled,
        "line_tile": line.tile,
        "reminder": reminder.filled,
    }
    assert actual == scen["expected"]


def test_fill_tile_mismatch_raises():
    line = SingleTileLine(1, 2, TILE)
    other = SingleTileLine(1, 1, OTHER_TILE)
    with pytest.raises(AttributeError):
        line.fill(other)


scenarios_extend = [
    {
        "name": "extend empty line",
        "line_filled": 0,
        "line_tile": None,
        "other_filled": 1,
        "other_tile": TILE,
        "expected": {
            "line_filled": 1,
            "line_size": 1,
            "line_tile": TILE,
        },
    },
    {
        "name": "extend within size",
        "line_filled": 1,
        "line_size": 5,
        "line_tile": TILE,
        "other_filled": 1,
        "other_tile": TILE,
        "expected": {
            "line_filled": 2,
            "line_size": 5,
            "line_tile": TILE,
        },
    },
    {
        "name": "extend over size",
        "line_filled": 1,
        "line_size": 2,
        "line_tile": TILE,
        "other_filled": 3,
        "other_tile": TILE,
        "expected": {
            "line_filled": 4,
            "line_size": 4,
            "line_tile": TILE,
        },
    },
    {
        "name": "extend within size other extra size",
        "line_filled": 1,
        "line_size": 2,
        "line_tile": TILE,
        "other_filled": 3,
        "other_size": 6,
        "other_tile": TILE,
        "expected": {
            "line_filled": 4,
            "line_size": 6,
            "line_tile": TILE,
        },
    },
]


@pytest.mark.parametrize("scen", scenarios_extend, ids=(scen["name"] for scen in scenarios_extend))
def test_extend(scen):
    line_filled, line_size, line_tile = scen.get("line_filled", 0), scen.get("line_size"), scen.get("line_tile")
    other_filled, other_size, other_tile = scen.get("other_filled", 0), scen.get("other_size"), scen.get("other_tile")

    line = SingleTileLine(line_filled, line_size, line_tile)
    other = SingleTileLine(other_filled, other_size, other_tile)
    line.extend(other)

    actual = {
        "line_filled": line.filled,
        "line_size": line.size,
        "line_tile": line.tile,
    }
    assert actual == scen["expected"]


scenarios_flush = [
    {
        "name": "flush empty line",
        "line_filled": 0,
        "line_size": 1,
        "line_tile": None,
        "expected": {
            "line_filled": 0,
            "line_size": 1,
            "line_tile": None,
            "returned_tile": None,
        },
    },
    {
        "name": "flush not full",
        "line_filled": 0,
        "line_size": 1,
        "line_tile": TILE,
        "expected": {
            "line_filled": 0,
            "line_size": 1,
            "line_tile": TILE,
            "returned_tile": None,
        },
    },
    {
        "name": "flush full",
        "line_filled": 2,
        "line_size": 2,
        "line_tile": TILE,
        "expected": {
            "line_filled": 0,
            "line_size": 2,
            "line_tile": None,
            "returned_tile": TILE,
        },
    },
]


@pytest.mark.parametrize("scen", scenarios_flush, ids=(scen["name"] for scen in scenarios_flush))
def test_flush(scen):
    line_filled, line_size, line_tile = scen.get("line_filled", 0), scen.get("line_size"), scen.get("line_tile")
    line = SingleTileLine(line_filled, line_size, line_tile)
    returned_tile = line.flush()

    actual = {
        "line_filled": line.filled,
        "line_size": line.size,
        "line_tile": line.tile,
        "returned_tile": returned_tile,
    }
    assert actual == scen["expected"]


@pytest.fixture
def line() -> SingleTileLine:
    return SingleTileLine(1, 2, Tile.BLACK)


def test_reset(line: SingleTileLine):
    line.reset()

    assert line.filled == 0
    assert line.size == 2
    assert line.tile == Tile.BLACK


def test_reset_with_tile(line: SingleTileLine):
    line.reset(reset_tile=True)

    assert line.filled == 0
    assert line.size == 2
    assert line.tile == None


def test_get_one(line: SingleTileLine):
    tile = line.get_one()

    assert tile == Tile.BLACK
    assert line.filled == 0
    assert line.size == 2
    assert line.tile == Tile.BLACK


def test_get_one_from_empty(line: SingleTileLine):
    line.get_one()
    with pytest.raises(RuntimeError):
        line.get_one()
