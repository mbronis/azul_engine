from email import message
from os import stat
from typing import Tuple
import pytest

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame


@pytest.fixture
def azul_game_state():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players=num_players, wall_type=wall_type, rules=rules)
    state = game.reset(seed=1)
    return game, state


def test_reset():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players=num_players, wall_type=wall_type, rules=rules)
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
    game = AzulGame(num_players=num_players, wall_type=wall_type, rules=rules)
    game.reset(seed=None)
    game.fill_factories()

    assert game.terminated == True
    assert sum(f.total_filled for f in game.factories) == len(Tile) * rules.tiles_count
    assert [f.total_filled for f in game.factories] == [4, 4, 2, 0, 0]  # only valid if len(Tile) == 5


def test_draw_from_factory(azul_game_state: Tuple[AzulGame, dict]):
    game, state = azul_game_state
    move = {
        "factory_no": 1,
        "tile": Tile.BLACK,
        "board_no": 0,
        "row": 0,
    }
    state, reward, executed, _ = game.action_draw_from_factory(**move)

    assert executed
    assert reward == 0.0
    assert state["game"] == {"phase": "factory", "round": 0}
    assert game.boards[0].pattern_lines.get_state()[0] == ("B", 1, 1)
    assert game.boards[0].floor_line.get_state()["tiles"][Tile.BLACK.value] == (1, 1)
    assert game.factories[1].get_state()[Tile.BLACK.value][0] == 0
    assert game.factories[1].total_filled == 0
    assert game.mid_factory.total_filled == 2
