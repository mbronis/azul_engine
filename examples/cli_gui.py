from src.gui.cli import CliGui, Window


c = CliGui(20, 50)
w = Window.from_string_lines(
    lines=[
        "xxxxxxxxxx",
        "xxxxxxxxxx",
        "xxxxxxxxxx",
    ],
    with_boarder=True,
    title="nice",
)
c.add(w, (5, 10))
c.show()
