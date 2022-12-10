from src.env.board.rules import AzulRules
from src.env.tiles import MultiTileLine, Tile, SingleTileLine
from src.env.board.board import Board
from src.env.walls import get_wall
from src.env.states.game_state import GameState


class AzulGame:
    def __init__(self, rules: AzulRules) -> None:
        wall = get_wall(rules.wall_type)
        self.boards = [Board(wall)] * rules.num_players
        self.tiles_bag = self._init_tiles_bag(tiles_count=rules.tiles_count)
        self.factories = [MultiTileLine()] * rules.num_factories
        self.mid_factory = MultiTileLine()
        self.discarded = MultiTileLine()

        self.factory_size: int = rules.factory_size
        self.terminated: bool = None

    def _init_tiles_bag(self, tiles_count: int) -> MultiTileLine:
        tiles = MultiTileLine()
        for tile in Tile:
            l = SingleTileLine(tile=tile, size=tiles_count)
            tiles.extend(l)
        return tiles

    def reset(self, seed: int = 1234) -> None:
        for board in self.boards:
            board.reset()
        self.tiles_bag.fill_max()
        for factory in self.factories:
            factory.reset()
        self.mid_factory.reset()
        self.discarded.reset()

        self.terminated = False

    def get_state(self) -> GameState:
        # TODO: implement
        pass
