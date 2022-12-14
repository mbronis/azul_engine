from typing import Tuple
from src.gui.cli import Window, CliGui


class AzulCliGui(CliGui):
    def __init__(self, x: int = 24, y: int = 90) -> None:
        super().__init__(x, y)

    @staticmethod
    def players_to_canvas_shape(num_players: Tuple[int, int]):
        """Helper method for AzulCliGui init"""
        shapes = {
            1: (16, 68),
            2: (16, 90),
            3: (26, 90),
            4: (26, 90),
        }
        return shapes[num_players]

    def draw_state(self, state: dict, text: str = None) -> None:
        """Updates image with state data"""
        title = self._draw_title()
        factories = self._draw_factories(state)
        legend = self._draw_legend()
        boards = [self._draw_board(b) for b in state["boards"].values()]
        dialog_box = self._draw_dialog_box(text)

        self.reset_canvas()
        self.add(title, (0, 2))
        self.add(factories, (2, 2))
        for i, board in enumerate(boards):
            x_offset = 2 + (1 + board.shape[0]) * (i > 1)
            y_offset = 4 + factories.shape[1] + 2 + (2 + board.shape[1]) * (i % 2 == 1)
            self.add(board, (x_offset, y_offset))
        self.add(legend, (2, 8 + factories.shape[1] + (board.shape[1] + 2) * (1 + (len(boards) > 1))))
        self.add(dialog_box, (4 + (board.shape[0]) * (1 + (len(boards) > 2)), 2))

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
        lines.append(f'1p   {"*" if state["game"]["mid_has_1p_token"] else "."}')
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string_lines(lines, with_boarder=True, title="Factories")

    def _draw_legend(self) -> Window:
        lines = ["u - blue", "y - yellow", "r - red", "b - black", "s - snow", "* - 1p token"]
        width = max(15, max(len(l) for l in lines))
        lines.append("-" * width)
        lines.extend(["x - required", "X - filled"])
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string_lines(lines, with_boarder=True, title="Legend")

    def _draw_board(self, board_state: dict) -> Window:
        score = self._draw_score(board_state)
        has_1p = self._draw_1p(board_state)
        pattern_lines = self._draw_pattern_lines(board_state)
        wall = self._draw_wall(board_state)
        floor = self._draw_floor(board_state)

        canvas = Window.canvas(8, 20, title=board_state["player_name"])
        canvas.add(score, (1, 2))
        canvas.add(has_1p, (1, score.shape[1] + 5))
        canvas.add(pattern_lines, (2, 2))
        canvas.add(wall, (2, pattern_lines.shape[1] + 5))
        canvas.add(floor, (wall.shape[0] + 3, 2))
        return canvas

    def _draw_score(self, board_state: dict) -> Window:
        score = str(board_state["score"]).ljust(3, " ")
        return Window.from_string_lines(f"score: {score}")

    def _draw_1p(self, board_state: dict) -> Window:
        has_1p = board_state["floor_line"]["has_1p_token"]
        return Window.from_string_lines(f"1p [{'*' if has_1p else ' '}]")

    def _draw_pattern_lines(self, board_state: dict) -> Window:
        def parse_pattern_line(pattern_line: dict) -> str:
            tile, filled, size = pattern_line
            return "." * (size - filled) + (tile if tile else ".") * filled

        lines = []
        for pattern_line in board_state["pattern_lines"]:
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
        return Window.from_string_lines(wall_lines)

    def _draw_floor(self, board_state: dict) -> Window:
        floor_state = board_state["floor_line"]
        floor_size = floor_state["size"]
        floor_fill = sum(fill for (fill, _) in floor_state["tiles"].values())
        floor_fill += int(floor_state["has_1p_token"])

        line = ("x" * floor_fill).ljust(floor_size, ".")
        line = "floor:  " + line
        return Window.from_string_lines(line)

    def _draw_dialog_box(self, text: str = None) -> Window:
        dialog_box = Window.canvas(1, self.image.shape[1] - 6)
        if text:
            text_box = Window.from_string_lines(text)
            dialog_box.add(text_box, (1, 2))
        return dialog_box
