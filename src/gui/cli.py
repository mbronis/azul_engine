from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Window:
    lines: List[List[str]]

    @classmethod
    def from_string(cls, lines: List[str], with_boarder: bool = False, title: str = None) -> Window:
        lines = [lines] if isinstance(lines, str) else lines
        w = Window(lines=[[*l] for l in lines])
        if with_boarder:
            w.add_boarder()
        if title:
            w.add_title(title)
        return w

    @property
    def shape(self) -> Tuple[int, int]:
        return len(self.lines), len(self.lines[0])

    def __getitem__(self, index: int) -> List[str]:
        return self.lines[index]

    def add_boarder(self):
        def get_char(pos: Tuple[int, int]) -> str:
            xx, yy = pos
            if pos in corners:
                return "+"
            if (xx == 0) or (xx == x):
                return "-"
            if (yy == 0) or (yy == y):
                return "|"
            return self.lines[xx - 1][yy - 1]

        x, y = self.shape
        x += 1
        y += 1
        corners = [(0, 0), (x, 0), (0, y), (x, y)]
        boarder_lines: List[str] = []
        for xx in range(x + 1):
            row = []
            for yy in range(y + 1):
                row.append(get_char((xx, yy)))
            boarder_lines.append(row)
        boarder_lines = [[*l] for l in boarder_lines]
        self.lines = boarder_lines

    def add(self, w: Window, offset: Tuple[int, int]):
        ox, oy = offset
        for x, row in enumerate(w.lines):
            for y, char in enumerate(row):
                self.lines[x + ox][y + oy] = char

    def add_title(self, title: str):
        _, y = self.shape
        title = title[: y - 4]
        t = Window.from_string(title, with_boarder=False)
        self.add(t, (0, 2))


class CliGui:
    def __init__(self, x: int, y: int, fill: str = " ") -> None:
        self.x, self.y = x, y
        self.fill = fill
        self.image: Window = None
        self.make_canvas()

    def make_canvas(self) -> None:
        image_string = []
        for _ in range(self.x):
            row = []
            for _ in range(self.y):
                row.append(self.fill)
            image_string.append("".join(row))
        self.image = Window.from_string(image_string, with_boarder=True)

    def add(self, w: Window, offset: Tuple[int, int]):
        self.image.add(w, offset)

    def render(self) -> str:
        r = ""
        for row in self.image.lines:
            r += "".join(row)
            r += "\n"
        return r

    def show(self):
        os.system("cls||clear")
        print(self.render())
