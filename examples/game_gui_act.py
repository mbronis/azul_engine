from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame
from src.gui.azul_cli import AzulCliGui


NUM_PLAYERS = 4


def azul_game():
    wall_type = "fixed"
    rules = get_rules("standard")
    game = AzulGame(num_players=NUM_PLAYERS, wall_type=wall_type, rules=rules)
    state = game.reset(seed=None)
    return game, state


game, state = azul_game()
a = {
    "factory_no": 1,
    "tile": Tile.BLACK,
    "board_no": 0,
    "row": 0,
}
state, reward, executed = game.action_draw_from_factory(**a)

c = AzulCliGui(*AzulCliGui.players_to_canvas_shape(NUM_PLAYERS))
c.draw_state(state)
c.show()
