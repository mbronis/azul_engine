from src.gui.azul_cli import AzulCliGui


def test_azul_cli_render():
    c = AzulCliGui()

    s = {
        "factories": {
            "f_0": {"U": (1, 1), "Y": (1, 1), "R": (0, 1), "B": (1, 1), "S": (1, 1)},
            "f_1": {"U": (0, 1), "Y": (0, 1), "R": (2, 2), "B": (0, 2), "S": (0, 1)},
            "f_2": {"U": (2, 2), "Y": (0, 1), "R": (1, 1), "B": (0, 1), "S": (1, 1)},
            "f_3": {"U": (1, 1), "Y": (0, 1), "R": (1, 1), "B": (2, 2), "S": (0, 1)},
            "f_4": {"U": (1, 1), "Y": (1, 1), "R": (0, 1), "B": (0, 1), "S": (2, 2)},
        },
        "mid_factory": {"U": (2, 2), "Y": (1, 1), "R": (0, 1), "B": (3, 3), "S": (0, 1)},
        "boards": {
            "board_1": {
                "score": 28,
                "player_name": "Player 1",
                "wall": {
                    "filled": [
                        ["U", "Y", ".", ".", "."],
                        ["S", ".", ".", ".", "."],
                        [".", ".", "U", ".", "."],
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
                "pattern_lines": [("B", 1, 1), (None, 0, 2), ("R", 1, 3), (None, 0, 4), ("S", 3, 5)],
                "floor_line": {"size": 7, "tiles": {"U": (0, 1), "Y": (2, 2), "R": (1, 1), "B": (0, 1), "S": (0, 1)}},
            },
            "board_2": {
                "score": 35,
                "player_name": "Player 2",
                "wall": {
                    "filled": [
                        [".", ".", ".", "B", "."],
                        [".", ".", ".", "R", "B"],
                        [".", ".", "U", "Y", "."],
                        [".", ".", ".", "U", "."],
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
                "pattern_lines": [(None, 0, 1), ("U", 2, 2), ("R", 2, 3), (None, 0, 4), (None, 0, 5)],
                "floor_line": {"size": 7, "tiles": {"U": (1, 1), "Y": (0, 2), "R": (0, 1), "B": (0, 1), "S": (0, 1)}},
            },
        },
    }
    c.draw_state(s)
    c.show()