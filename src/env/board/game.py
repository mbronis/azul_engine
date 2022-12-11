import random
from typing import Tuple

from src.env.board.rules import AzulRules
from src.env.tiles import Tile
from src.env.lines import SingleTileLine, MultiTileLine
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

    def reset(self, seed: int = None) -> dict:
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

        # TODO: move to method for checking terminated state (with add check for row fill in wall)
        self.terminated = self.tiles_bag.total_filled == 0

    def _set_random(self, seed: int) -> None:
        random.seed(seed)

    def get_state(self) -> dict:
        state = {}
        state["boards"] = {f"board_{i}": b.get_state() for i, b in enumerate(self.boards)}
        state["factories"] = {f"f{i}": f.get_state() for i, f in enumerate(self.factories)}
        state["mid_factory"] = self.mid_factory.get_state()
        return state

    def action_draw_from_factory(self, factory_no: int, tile: Tile, board_no: int, row: int) -> bool:
        """Draws all tiles from selected factory and tries to add to a pattern line.

        Returns
        -------
        state : dict
            game state after performing the move
        reward : float
            reward for the move
        executed : bool
            if the move was valid and was performed
        """
        ILLEGAL_MOVE_PENALTY = -10.0
        board = self.boards[board_no]
        if not board.can_fill_pattern_line(row, tile):
            return self.get_state(), ILLEGAL_MOVE_PENALTY, False
        factory = (self.factories + [self.mid_factory])[factory_no]
        tiles_line = factory.get_all(tile)
        board.fill_pattern_line(row, tiles_line)
        return self.get_state(), 0.0, True
