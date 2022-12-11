from src.env.board.rules import get_rules
from src.env.board.game import AzulGame


def azul_game():
    num_players = 2
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players=num_players, wall_type=wall_type, rules=rules)
    state = game.reset(seed=1)
    return game, state


game, state = azul_game()
print(state)
