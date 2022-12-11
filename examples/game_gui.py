from src.gui.cli import AzulCliGui


c = AzulCliGui()

s = {
    "factories": {
        "f0": {"u": 1, "y": 1, "r": 0, "b": 1, "s": 1},
        "f1": {"u": 0, "y": 0, "r": 2, "b": 0, "s": 0},
        "f2": {"u": 2, "y": 0, "r": 1, "b": 0, "s": 1},
        "f3": {"u": 1, "y": 0, "r": 1, "b": 2, "s": 0},
        "f4": {"u": 1, "y": 1, "r": 0, "b": 0, "s": 2},
    }
}
c.draw_state(s)
c.show()
