.PHONY: default init serve pytest format lint sort run kik

default: pytest mut lint sort format

init:
	poetry install

serve:
	bash ./scripts/http_server.sh

pytest:
	bash ./scripts/coverage_pytest.sh

bdd:
	bash ./scripts/coverage_mamba.sh

mut:
	bash ./scripts/mutmut.sh

format:
	bash ./scripts/black.sh

lint:
	bash ./scripts/flake8.sh

sort:
	bash ./scripts/isort.sh

run:
	poetry run python bot.py

kik:
	python kik_bot.py