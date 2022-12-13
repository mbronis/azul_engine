from typing import Tuple

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame
from src.gui.azul_cli import AzulCliGui


NUM_PLAYERS = 1


def init_game() -> Tuple[AzulGame, dict]:
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players=NUM_PLAYERS, wall_type=wall_type, rules=rules)
    state = game.reset(seed=None)
    return game, state


def invalid_action_prompt(action: dict) -> str:
    return f"Invalid action: {action}"


if __name__ == "__main__":
    game, state = init_game()
    gui = AzulCliGui(*AzulCliGui.players_to_canvas_shape(NUM_PLAYERS))

    gui.draw_state(state, "Welcome to Azul Engine :D")
    gui.show()
    while True:
        factory_no, tile, row = input("input action (factory_no, tile, row):.. ").split()
        factory_no, tile, row = int(factory_no), Tile(tile.upper()), int(row)
        action = {"factory_no": factory_no, "tile": tile, "row": row, "board_no": 0}
        state, reward, executed, info = game.action_draw_from_factory(**action)
        gui.draw_state(state, info)
        gui.show()
