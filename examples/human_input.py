from typing import Tuple

from src.env.tiles import Tile
from src.env.board.rules import get_rules
from src.env.board.game import AzulGame
from src.env.scoring import Scorer
from src.gui.azul_cli import AzulCliGui
from src.env.messages import get_messages


NUM_PLAYERS = 2
SEED = 1


def init_game() -> Tuple[AzulGame, dict]:
    wall_type = "fixed"
    rules = get_rules("standard")
    scorer = Scorer(rules)
    messages = get_messages("default")
    game = AzulGame(num_players=NUM_PLAYERS, wall_type=wall_type, rules=rules, scorer=scorer, messages=messages)
    state = game.reset(seed=SEED)
    return game, state


def input_prompt(state):
    f_num = len(state["factories"])
    tiles = "/".join([t.value.lower() for t in Tile])
    rows_num = len(state["boards"]["board_0"]["pattern_lines"]) - 1

    prefix = "Draw from factory (input: "

    return (
        prefix + f"factory_no <0-{f_num-1} or {f_num} for mid>):",
        prefix + f"tile <{tiles}>):",
        prefix + f"row <0-{rows_num} or enter for floor>):",
    )


if __name__ == "__main__":
    game, state = init_game()
    gui = AzulCliGui(*AzulCliGui.players_to_canvas_shape(NUM_PLAYERS))

    gui.draw_state(state, game.messages.welcome_message)
    gui.show()
    while True:
        prompt_factory, prompt_tile, prompt_row = input_prompt(state)
        factory_no = int(input(prompt_factory))
        tile = Tile(input(prompt_tile).upper())
        row = input(prompt_row)
        row = None if not row else int(row)
        # factory_no, tile, row = int(inputs[0]), Tile(inputs[1].upper()), None if len(inputs) == 2 else int(inputs[2])
        action = {"factory_no": factory_no, "tile": tile, "row": row, "board_no": 0}
        state, reward, executed, info = game.action_draw_from_factory(**action)
        gui.draw_state(state, info)
        gui.show()
