test: ## run unittests with code coverage
test:
	pytest --cov-report term-missing --cov src/.*

cli: ## cli render testing
cli:
	python examples/cli_gui.py

game: ## game testing
game:
	python examples/game.py

game_cli: ## cli render testing
game_cli:
	python examples/game_gui.py