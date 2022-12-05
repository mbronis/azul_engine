import pytest

from src.env.tiles import Tile
from src.env.board.wall import Wall, FixedWall
from src.env.rules.wall import can_fill


def fill(w: Wall):
    w._filled[0][0] = Tile.BLUE
    w._filled[1][2] = Tile.YELLOW


@pytest.fixture
def wall() -> Wall:
    w = Wall()
    fill(w)
    return w


@pytest.fixture
def fixed_wall() -> FixedWall:
    w = FixedWall()
    fill(w)
    return w


scenarios = [
    {
        "name": "Can fill empty slot",
        "row": 1,
        "col": 1,
        "tile": Tile.BLUE,
        "expected": True,
    },
    {
        "name": "Can fill other tile",
        "row": 0,
        "col": 1,
        "tile": Tile.YELLOW,
        "expected": True,
    },
    {
        "name": "Can't fill non-empty slot",
        "row": 0,
        "col": 0,
        "tile": Tile.BLUE,
        "expected": False,
    },
    {
        "name": "Can't fill same tile in row",
        "row": 0,
        "col": 2,
        "tile": Tile.BLUE,
        "expected": False,
    },
    {
        "name": "Can't fill same tile in col",
        "row": 0,
        "col": 2,
        "tile": Tile.YELLOW,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_can_fill(scen, wall: Wall):
    actual = can_fill(wall, scen["row"], scen["col"], scen["tile"])
    assert actual == scen["expected"]


scenarios_fixed = scenarios + [
    {
        "name": "Can't fill other tile if not expected",
        "row": 0,
        "col": 1,
        "tile": Tile.RED,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios_fixed, ids=(scen["name"] for scen in scenarios_fixed))
def test_can_fill_fixed(scen, fixed_wall: FixedWall):
    actual = can_fill(fixed_wall, scen["row"], scen["col"], scen["tile"])
    assert actual == scen["expected"]
