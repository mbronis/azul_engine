from src.gui.azul_cli import AzulCliGui


c = AzulCliGui()

s = {
    "factories": {
        "f_0": {"u": 1, "y": 1, "r": 0, "b": 1, "s": 1},
        "f_1": {"u": 0, "y": 0, "r": 3, "b": 1, "s": 0},
        "f_2": {"u": 2, "y": 0, "r": 1, "b": 0, "s": 1},
        "f_3": {"u": 1, "y": 0, "r": 1, "b": 2, "s": 0},
        "f_4": {"u": 1, "y": 1, "r": 0, "b": 0, "s": 2},
    },
    "mid_factory": {"u": 0, "y": 0, "r": 0, "b": 0, "s": 0},
    "boards": {
        "board_1": {
            "score": 0,
            "wall": {
                "filled": [
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."],
                    [".", ".", ".", ".", "."],
                ],
                "expected": [
                    ["u", "y", "r", "b", "s"],
                    ["s", "u", "y", "r", "b"],
                    ["b", "s", "u", "y", "r"],
                    ["r", "b", "s", "u", "y"],
                    ["y", "r", "b", "s", "u"],
                ],
            },
            "pattern_lines": {
                "pattern_line_0": {"b": 1},
                "pattern_line_1": {None: 0},
                "pattern_line_2": {None: 0},
                "pattern_line_3": {None: 0},
                "pattern_line_4": {None: 0},
            },
            "floor_line": {"u": 0, "y": 0, "r": 0, "b": 1, "s": 0},
        }
    },
}
c.draw_state(s)
c.show()
