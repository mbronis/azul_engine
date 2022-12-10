import random

from src.env.board.rules import AzulRules
from src.env.tiles import MultiTileLine, Tile, SingleTileLine
from src.env.board.board import Board
from src.env.walls import get_wall
from src.env.states.game_state import GameState
from src.env.scoring import Scorer


class AzulGame:
    def __init__(self, num_players: int, wall_type: str, rules: AzulRules) -> None:
        # TODO: inject dependency
        self.scorer = Scorer(rules)

        self.terminated: bool = None
        self.num_players = num_players
        self.factory_size: int = rules.factory_size
        self.num_factories = rules.get_num_factories(num_players)

        wall = get_wall(wall_type)
        self.boards = [Board(wall) for _ in range(self.num_players)]
        self.factories = [MultiTileLine() for _ in range(self.num_factories)]
        self.mid_factory = MultiTileLine()
        self.discarded = MultiTileLine()
        self.tiles_bag = MultiTileLine()
        for tile in Tile:
            l = SingleTileLine(tile=tile, size=rules.tiles_count, filled=0)
            self.tiles_bag.extend(l)

    def reset(self, seed: int = 1234) -> GameState:
        self.terminated = False
        self._set_random(seed)

        for board in self.boards:
            board.reset()
        for factory in self.factories:
            factory.reset()
        self.mid_factory.reset()
        self.discarded.reset()

        self.tiles_bag.fill_max()
        self.fill_factories()

        return self.get_state()

    def fill_factories(self):
        for factory in self.factories:
            tiles = self.tiles_bag.get_random(n=self.factory_size)
            factory.merge(tiles)

    def _set_random(self, seed: int) -> None:
        random.seed(seed)

    def get_state(self) -> GameState:
        # TODO: implement
        return {}, {}
