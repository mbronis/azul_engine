from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame


def print_state(s):
    for k, v in state.items():
        print(f"{k}:\n{v}")


def azul_game():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players, wall_type, rules)
    state = game.reset(seed=1)
    return game, state


game, state = azul_game()
print_state(state)

a = {
    "factory_no": 1,
    "tile": Tile.BLACK,
    "board_no": 0,
    "row": 0,
}
state, reward, executed = game.action_draw_from_factory(**a)
print("---------------------------")
print_state(state)
