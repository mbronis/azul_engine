import pytest

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame


def test_reset():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players, wall_type, rules)
    state, info = game.reset(seed=1)

    assert game.terminated == False
    assert len(Tile) * rules.tiles_count == game.tiles_bag.total_filled + sum(f.total_filled for f in game.factories)
