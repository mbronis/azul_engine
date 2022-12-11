from src.gui.cli import Window, CliGui


class AzulCliGui(CliGui):
    def draw_state(self, state: dict) -> None:
        """Updates image with state data"""
        title = self._draw_title()
        factories = self._draw_factories(state)
        legend = self._draw_legend()

        self.make_canvas()
        self.add(title, (0, 2))
        self.add(factories, (2, 2))
        self.add(legend, (factories.shape[0] + 3, 2))

    def _draw_title(self) -> Window:
        return Window.from_string("Azul Game")

    def _draw_factories(self, state: dict) -> Window:
        def parse_factory_state(factory_state: dict) -> str:
            return " ".join([str(v) if v else "." for v in factory_state.values()])

        width = 15
        lines = ["     u y r b s "]
        for factory_name, factory_state in state["factories"].items():
            state_string = parse_factory_state(factory_state)
            factory_line = f"{factory_name}  {state_string}"
            lines.append(factory_line)
        lines.append("-" * width)
        lines.append(f"mid  {parse_factory_state(state['mid_factory'])}")
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string(lines, with_boarder=True, title="Factories")

    def _draw_legend(self) -> Window:
        lines = ["u - blue", "y - yellow", "r - red", "b - black", "s - snow"]
        width = max(15, max(len(l) for l in lines) + 3)
        lines.append("-" * width)
        lines.extend(["x - required", "X - filled"])
        lines = [l.ljust(width, " ") for l in lines]
        return Window.from_string(lines, with_boarder=True, title="Legend")
