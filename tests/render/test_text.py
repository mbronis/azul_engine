from src.gui.text import print_state

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame
from src.env.scoring import Scorer
from src.env.messages import get_messages


def azul_game():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    scorer = Scorer(rules)
    messages = get_messages("default")
    game = AzulGame(num_players=num_players, wall_type=wall_type, rules=rules, scorer=scorer, messages=messages)
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
state, reward, executed, message = game.action_draw_from_factory(**a)
print("---------------------------")
print(f"action: {a}")
print("---------------------------")
print_state(state)
