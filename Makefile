.PHONY: default init bdd test format sort lint run

default: test lint sort format

init:
	poetry install

serve:
	bash ./scripts/serve.sh

test:
	bash ./scripts/mamba.sh

format:
	bash ./scripts/format.sh

lint:
	bash ./scripts/lint.sh

sort:
	bash ./scripts/sort.sh

run:
	poetry run python bot.py