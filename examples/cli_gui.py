from src.gui.cli import CliGui, Window


c = CliGui()
w = Window.from_string(
    lines=[
        "xxxxx",
        "xxxxx",
        "xxxxx",
    ]
)
wb = Window.add_boarder(w)
c.add(wb, (5, 10))
c.show()
