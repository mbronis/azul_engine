from os import stat
import pytest

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame


@pytest.fixture
def azul_game():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players, wall_type, rules)
    state = game.reset(seed=1)
    return game, state


def test_reset():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players, wall_type, rules)
    game.reset(seed=None)

    assert game.terminated == False
    assert len(Tile) * rules.tiles_count == game.tiles_bag.total_filled + sum(f.total_filled for f in game.factories)
    assert game.mid_factory.total_filled == 0
    assert game.discarded.total_filled == 0


def test_factories_fill_when_depleted():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    rules.get_num_factories = lambda x: 5
    rules.factory_size = 4
    rules.tiles_count = 2
    game = AzulGame(num_players, wall_type, rules)
    game.reset(seed=None)

    assert game.terminated == True
    assert sum(f.total_filled for f in game.factories) == len(Tile) * rules.tiles_count
    assert [f.total_filled for f in game.factories] == [4, 4, 2, 0, 0]  # only valid if len(Tile) == 5


def test_draw_from_factory(azul_game: AzulGame):
    game, state = azul_game
    move = {
        "factory_no": 1,
        "tile": Tile.BLACK,
        "board_no": 0,
        "row": 0,
    }
    state, reward, executed = game.action_draw_from_factory(**move)

    assert executed
    assert reward == 0.0
    assert state["boards"]["board_0"]["pattern_lines"]["pattern_line_0"] == (Tile.BLACK.value, 1, 1)
    assert state["boards"]["board_0"]["floor_line"][Tile.BLACK.value] == (1, 1)
    assert state["factories"]["f_1"][Tile.BLACK.value][0] == 0
    assert sum(v[0] for v in state["factories"]["f_1"].values()) == 2
