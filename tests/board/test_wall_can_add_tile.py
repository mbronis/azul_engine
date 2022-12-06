import pytest

from src.env.tiles import Tile
from src.env.board.wall import Wall
from src.env.walls import FixedWall, FreeWall


def fill(w: Wall):
    w._filled[0][0] = Tile.BLUE
    w._filled[1][2] = Tile.YELLOW


@pytest.fixture
def wall() -> FreeWall:
    w = FreeWall()
    fill(w)
    return w


@pytest.fixture
def fixed_wall() -> FixedWall:
    w = FixedWall()
    fill(w)
    return w


scenarios = [
    {
        "name": "Can add tile to empty slot",
        "row": 1,
        "col": 1,
        "tile": Tile.BLUE,
        "expected": True,
    },
    {
        "name": "Can add tile with other tile neighbor",
        "row": 0,
        "col": 1,
        "tile": Tile.YELLOW,
        "expected": True,
    },
    {
        "name": "Can't add tile to non-empty slot",
        "row": 0,
        "col": 0,
        "tile": Tile.BLUE,
        "expected": False,
    },
    {
        "name": "Can't add tile if same tile in row",
        "row": 0,
        "col": 2,
        "tile": Tile.BLUE,
        "expected": False,
    },
    {
        "name": "Can't add tile if same tile in col",
        "row": 0,
        "col": 2,
        "tile": Tile.YELLOW,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_can_add_tile(scen, wall: Wall):
    actual = wall.can_add_tile(scen["row"], scen["col"], scen["tile"])
    assert actual == scen["expected"]


scenarios_fixed = scenarios + [
    {
        "name": "Can't add tile if other tile is not expected",
        "row": 0,
        "col": 1,
        "tile": Tile.RED,
        "expected": False,
    },
]


@pytest.mark.parametrize("scen", scenarios_fixed, ids=(scen["name"] for scen in scenarios_fixed))
def test_can_add_tile_fixed(scen, fixed_wall: FixedWall):
    actual = fixed_wall.can_add_tile(scen["row"], scen["col"], scen["tile"])
    assert actual == scen["expected"]
