"""Configuration of the game"""
from typing import List
from dataclasses import dataclass, field


@dataclass
class AzulRules:
    """Provides configuration for Azul game.


    Arguments
    ---------
    tiles_count : int
        total number of tiles of each type used in a game
    factory_size : int
        number of tiles in each factory
    factories_to_players : dict[int, int]
        maps number of players to number of factories used
    floor_len : int
        max number of tiles on floor
    points_self : int
        number of points for adding a tile to the wall
    points_neighbor : int
        number of points for each neighbor of added tile
    points_row_fill : int
        number of points for filling wall row
    points_col_fill : int
        number of points for filling wall column
    points_color_fill : int
        number of points for filling all tiles of one type
    floor_penalties : List[int]
        penalty for each tile on floor


    Attributes
    ----------
    num_factories : int
        Actual number of factories used in game
    """

    tiles_count: int = field(init=False)
    factory_size: int = field(init=False)
    factories_to_players: dict[int, int] = field(init=False)

    # wall tiling scores
    points_self: int = field(init=False)
    points_neighbor: int = field(init=False)
    points_row_fill: int = field(init=False)
    points_col_fill: int = field(init=False)
    points_color_fill: int = field(init=False)
    floor_penalties: List[int] = field(init=False)

    def get_num_factories(self, num_players: int) -> int:
        return self.factories_to_players[num_players]


@dataclass
class StandardAzulRules(AzulRules):
    """Standard Azul rulebook configuration."""

    tiles_count = 20
    factory_size = 4
    factories_to_players = {1: 3, 2: 5, 3: 7, 4: 9}

    points_self = 1
    points_neighbor = 1
    points_row_fill = 2
    points_col_fill = 5
    points_color_fill = 10
    floor_penalties = [-1, -1, -2, -2, -2, -3, -3]


def get_rules(rule_set_name: str = "standard") -> AzulRules:
    rule_sets = {
        "standard": StandardAzulRules(),
    }
    return rule_sets[rule_set_name]
