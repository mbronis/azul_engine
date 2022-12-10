import pytest

from src.env.tiles import Tile
from src.env.board.wall import Wall
from src.env.states.wall_state import WallState


@pytest.fixture
def wall_a() -> WallState:
    wall = Wall(
        size=5,
        filled=[
            [Tile.BLACK, Tile.BLUE, None, None, Tile.RED],
            [Tile.RED, None, None, None, None],
            [None, None, None, Tile.BLACK, None],
            [None, None, Tile.RED, None, Tile.BLACK],
            [Tile.SNOW, None, None, Tile.BLUE, None],
        ],
    )
    return wall.get_state()


scenarios = [
    {"name": "wall_a, 0, 0", "row": 0, "col": 0, "expected": (1, 1, 2)},
    {"name": "wall_a, 1, 0", "row": 1, "col": 0, "expected": (0, 1, 1)},
    {"name": "wall_a, 0, 1", "row": 0, "col": 1, "expected": (1, 0, 1)},
    {"name": "wall_a, 1, 1", "row": 1, "col": 1, "expected": (1, 1, 2)},
    {"name": "wall_a, 2, 0", "row": 2, "col": 0, "expected": (0, 2, 2)},
    {"name": "wall_a, 0, 2", "row": 0, "col": 2, "expected": (2, 0, 2)},
    {"name": "wall_a, 2, 1", "row": 2, "col": 1, "expected": (0, 0, 0)},
    {"name": "wall_a, 3, 0", "row": 3, "col": 0, "expected": (0, 1, 1)},
    {"name": "wall_a, 0, 3", "row": 0, "col": 3, "expected": (1, 0, 1)},
    {"name": "wall_a, 3, 2", "row": 3, "col": 2, "expected": (0, 0, 0)},
    {"name": "wall_a, 2, 3", "row": 2, "col": 3, "expected": (0, 0, 0)},
    {"name": "wall_a, 3, 3", "row": 3, "col": 3, "expected": (2, 2, 4)},
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_neighbor_wall_a(scen, wall_a: WallState):
    act_row = wall_a.count_neighbors_row(scen["row"], scen["col"])
    act_col = wall_a.count_neighbors_col(scen["row"], scen["col"])
    act_total = wall_a.count_neighbors(scen["row"], scen["col"])
    exp_row, exp_col, exp_total = scen["expected"]
    assert act_row == exp_row
    assert act_col == exp_col
    assert act_total == exp_total


@pytest.fixture
def wall_b() -> WallState:
    wall = Wall(
        size=5,
        filled=[
            [Tile.BLACK, None, Tile.BLUE, Tile.YELLOW, None],
            [None, None, None, None, None],
            [Tile.BLUE, None, None, None, None],
            [Tile.SNOW, None, None, None, None],
            [None, None, None, None, None],
        ],
    )
    return wall.get_state()


scenarios = [
    {"name": "wall_b, 0, 0", "row": 0, "col": 0, "expected": (0, 0, 0)},
    {"name": "wall_b, 0, 1", "row": 0, "col": 1, "expected": (3, 0, 3)},
    {"name": "wall_b, 0, 2", "row": 0, "col": 2, "expected": (1, 0, 1)},
    {"name": "wall_b, 0, 3", "row": 0, "col": 3, "expected": (1, 0, 1)},
    {"name": "wall_b, 0, 4", "row": 0, "col": 4, "expected": (2, 0, 2)},
    {"name": "wall_b, 0, 0", "row": 0, "col": 0, "expected": (0, 0, 0)},
    {"name": "wall_b, 1, 0", "row": 1, "col": 0, "expected": (0, 3, 3)},
    {"name": "wall_b, 2, 0", "row": 2, "col": 0, "expected": (0, 1, 1)},
    {"name": "wall_b, 3, 0", "row": 3, "col": 0, "expected": (0, 1, 1)},
    {"name": "wall_b, 4, 0", "row": 4, "col": 0, "expected": (0, 2, 2)},
]


@pytest.mark.parametrize("scen", scenarios, ids=(scen["name"] for scen in scenarios))
def test_neighbor_wall_b(scen, wall_b: WallState):
    act_row = wall_b.count_neighbors_row(scen["row"], scen["col"])
    act_col = wall_b.count_neighbors_col(scen["row"], scen["col"])
    act_total = wall_b.count_neighbors(scen["row"], scen["col"])
    exp_row, exp_col, exp_total = scen["expected"]
    assert act_row == exp_row
    assert act_col == exp_col
    assert act_total == exp_total


def test_get_tile_count_wall_a(wall_a: WallState):
    assert wall_a.get_tile_count(Tile.BLACK) == 3
    assert wall_a.get_tile_count(Tile.BLUE) == 2
    assert wall_a.get_tile_count(Tile.SNOW) == 1
    assert wall_a.get_tile_count(Tile.RED) == 3
    assert wall_a.get_tile_count(Tile.YELLOW) == 0


def test_get_tile_count_wall_a(wall_b: WallState):
    assert wall_b.get_tile_count(Tile.BLACK) == 1
    assert wall_b.get_tile_count(Tile.BLUE) == 2
    assert wall_b.get_tile_count(Tile.SNOW) == 1
    assert wall_b.get_tile_count(Tile.RED) == 0
    assert wall_b.get_tile_count(Tile.YELLOW) == 1
