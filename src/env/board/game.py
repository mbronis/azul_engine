from dataclasses import dataclass
import random
from typing import List
from enum import Enum

from src.env.board.rules import AzulRules
from src.env.tiles import Tile
from src.env.lines import SingleTileLine, MultiTileLine
from src.env.board.board import Board
from src.env.walls import get_wall
from src.env.scoring import Scorer
from src.env.messages import Messages


class GamePhase(Enum):
    """
    Describes different phases of Azul game.
    Defines possible actions.

    Values
    ------
        FACTORY
            Phase where tiles are taken from factories and placed in pattern lines
        WALL
            Phase where tiles are taken from pattern lines and placed in the wall.
        TERMINATED
            Game is complete, no more moves are possible.
    """

    FACTORY = "factory"
    WALL = "wall"
    TERMINATED = "terminated"


class AzulGame:
    def __init__(
        self,
        num_players: int,
        wall_type: str,
        rules: AzulRules,
        # scorer: Scorer,
        messages: Messages,
        player_names: List[str] = None,
    ) -> None:
        # TODO: inject dependencies (scorer, wall, ...)
        self.scorer = Scorer(rules)

        # init game params
        self.factory_size: int = rules.factory_size
        self.num_factories = rules.get_num_factories(num_players)
        self.num_players = num_players
        self.player_name = player_names
        if not player_names or (len(player_names) != num_players):
            self.player_name = [f"Player {i+1}" for i in range(num_players)]

        # init game components
        wall = get_wall(wall_type)
        floor_size = len(rules.floor_penalties)
        self.boards = [Board(wall, floor_size, name) for name in self.player_name]
        self.factories = [MultiTileLine() for _ in range(self.num_factories)]
        self.mid_factory = MultiTileLine()
        self.discarded = MultiTileLine()
        self.tiles_bag = MultiTileLine()
        for tile in Tile:
            l = SingleTileLine(tile=tile, size=rules.tiles_count, filled=0)
            self.tiles_bag.extend(l)

        # init game internals
        self.messages = messages
        self.phase: GamePhase = None
        self.round: int = None
        self.move: int = None

    @property
    def terminated(self) -> bool:
        return self.phase == GamePhase.TERMINATED

    def reset(self, seed: int = None) -> dict:
        self._set_random(seed)
        self.round, self.move = -1, -1

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
        if self.tiles_bag.total_filled == 0:
            self.phase = GamePhase.TERMINATED
            return

        self.phase = GamePhase.FACTORY
        self.round += 1
        for factory in self.factories:
            tiles = self.tiles_bag.get_random(n=self.factory_size)
            factory.merge(tiles)

    def _set_random(self, seed: int) -> None:
        random.seed(seed)

    def get_state(self) -> dict:
        state = {}
        state["game"] = {"phase": self.phase.value, "round": self.round, "move": self.move}
        state["boards"] = {f"board_{i}": b.get_state() for i, b in enumerate(self.boards)}
        state["factories"] = {f"f_{i}": f.get_state() for i, f in enumerate(self.factories)}
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
        message : str
            info about move execution
        """
        # TODO: get move penalties from env
        ILLEGAL_MOVE_PENALTY = -10.0
        board = self.boards[board_no]
        if not board.can_fill_pattern_line(tile, row):
            return (
                self.get_state(),
                ILLEGAL_MOVE_PENALTY,
                False,
                self.messages.action_draw_fail_board.format(row=row, tile=tile.value),
            )
        factory = (self.factories + [self.mid_factory])[factory_no]
        if not factory.has_tile(tile):
            return (
                self.get_state(),
                ILLEGAL_MOVE_PENALTY,
                False,
                self.messages.action_draw_fail_factory.format(factory_no=factory_no, tile=tile.value),
            )

        tiles_line, reminder = factory.get_all(tile)
        board.fill_pattern_line(tiles_line, row)
        self.mid_factory.merge(reminder)
        self.move += 1
        if self.all_factories_are_empty():
            self.phase = GamePhase.WALL
        return self.get_state(), 0.0, True, self.messages.action_draw_success

    def all_factories_are_empty(self) -> bool:
        return max(f.total_filled for f in self.factories + [self.mid_factory]) == 0
