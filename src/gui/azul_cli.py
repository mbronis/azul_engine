from src.gui.cli import Window, CliGui
from tests.tiles.test_single_tile_line import line


class AzulCliGui(CliGui):
    def __init__(self, x: int = 24, y: int = 80) -> None:
        super().__init__(x, y)

    def draw_state(self, state: dict) -> None:
        """Updates image with state data"""
        title = self._draw_title()
        factories = self._draw_factories(state)
        legend = self._draw_legend()
        board = self._draw_board(state["boards"]["board_1"])

        self.reset_canvas()
        self.add(title, (0, 2))
        self.add(factories, (2, 2))
        self.add(legend, (factories.shape[0] + 3, 2))
        self.add(board, (2, factories.shape[1] + 10))

    def _draw_title(self) -> Window:
        return Window.from_string_lines("Azul Game")

    def _draw_factories(self, state: dict) -> Window:
        def parse_factory_state(factory_state: dict) -> str:
            return " ".join([str(v[0]) if v[0] > 0 else "." for v in factory_state.values()])

        width = 15
        lines = ["     U Y R B S"]
        for factory_name, factory_state in state["factories"].items():
            state_string = parse_factory_state(factory_state)
            factory_line = f"{factory_name}  {state_string}"
            lines.append(factory_line)
        lines.append("-" * width)
        lines.append(f"mid  {parse_factory_state(state['mid_factory'])}")
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string_lines(lines, with_boarder=True, title="Factories")

    def _draw_legend(self) -> Window:
        lines = ["u - blue", "y - yellow", "r - red", "b - black", "s - snow"]
        width = max(15, max(len(l) for l in lines) + 3)
        lines.append("-" * width)
        lines.extend(["x - required", "X - filled"])
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string_lines(lines, with_boarder=True, title="Legend")

    def _draw_board(self, board_state: dict) -> Window:
        pattern_lines = self._draw_pattern_lines(board_state)
        wall = self._draw_wall(board_state)

        canvas = Window.canvas(8, 20, title=f"Score {board_state['score']}")
        canvas.add(pattern_lines, (2, 2))
        canvas.add(wall, (2, pattern_lines.shape[1] + 5))
        return canvas

    def _draw_pattern_lines(self, board_state: dict) -> Window:
        def parse_pattern_line(pattern_line: dict) -> str:
            tile, (filled, size) = list(pattern_line.items())[0]
            return "." * (size - filled) + (tile if tile else ".") * filled

        lines = []
        for pattern_line in board_state["pattern_lines"].values():
            lines.append(parse_pattern_line(pattern_line))

        width = max(len(l) for l in lines)
        lines = [l.rjust(width, " ") for l in lines]
        return Window.from_string_lines(lines)

    def _draw_wall(self, board_state: dict) -> Window:
        filled_lines = board_state["wall"]["filled"]
        wall_lines = board_state["wall"]["expected"]
        for x, row in enumerate(wall_lines):
            for y, _ in enumerate(row):
                if filled_lines[x][y] != ".":
                    wall_lines[x][y] = filled_lines[x][y]

        wall_lines = [" ".join(l) for l in wall_lines]
        return Window.from_string_lines(wall_lines, with_boarder=False)
