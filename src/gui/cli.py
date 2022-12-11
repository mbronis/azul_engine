from __future__ import annotations
import os
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Window:
    lines: List[List[str]]

    @classmethod
    def from_string(cls, lines: List[str], boarder: bool = True) -> Window:
        lines = [lines] if isinstance(lines, str) else lines
        return Window(lines=[[*l] for l in lines])

    @property
    def shape(self) -> Tuple[int, int]:
        return len(self.lines), len(self.lines[0])

    def __getitem__(self, index: int) -> List[str]:
        return self.lines[index]

    def add(self, w: Window, offset: Tuple[int, int]):
        ox, oy = offset
        for x, row in enumerate(w.lines):
            for y, char in enumerate(row):
                self.lines[x + ox][y + oy] = char

    @staticmethod
    def add_boarder(w: Window) -> Window:
        def get_char(pos: Tuple[int, int]) -> str:
            xx, yy = pos
            if pos in corners:
                return "+"
            if (xx == 0) or (xx == x):
                return "-"
            if (yy == 0) or (yy == y):
                return "|"
            return " "

        x, y = w.shape
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
        window = Window.from_string(boarder_lines)
        window.add(w, (1, 1))
        return window


class CliGui:
    def __init__(self, x: int = 20, y: int = 80, fill: str = ".") -> None:
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
            image_string.append(row)
        self.image = Window(image_string)

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


class AzulCliGui(CliGui):
    def draw_state(self, state: dict) -> None:
        """Updates image with state data"""
        title = self._draw_title()
        factories = self._draw_factories(state)

        self.add(title, (0, 0))
        self.add(factories, (2, 0))

    def _draw_title(self) -> Window:
        return Window.from_string("Azul Game")

    def _draw_factories(self, state: dict) -> Window:
        lines = ["--- uyrbs -"]
        for factory_name, factory_state in state["factories"].items():
            state_string = "".join([str(v) for v in factory_state.values()]) + "  "
            print(state_string)
            factory_line = f"{factory_name}: {state_string}"
            lines.append(factory_line)
        return Window.from_string(lines)
