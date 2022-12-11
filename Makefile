test: ## run unittests with code coverage
test:
	pytest --cov-report term-missing --cov src/.*

cli: ## cli render testing
cli:
	python examples/cli_gui.py

state: ## prints actual game state
state:
	python examples/state.py

game: ## game testing
game:
	python examples/game.py

game_cli: ## render fixed game state
game_cli:
	python examples/game_gui.py

game_act: ## render actual game state
game_act:
	python examples/game_gui_act.py