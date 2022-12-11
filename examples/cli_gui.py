from src.gui.cli import CliGui, Window


c = CliGui()
w = Window.from_string(
    lines=[
        "xxxxx",
        "xxxxx",
        "xxxxx",
    ],
    with_boarder=True,
    title="nice",
)
c.add(w, (5, 10))
c.show()
