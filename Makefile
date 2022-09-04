.PHONY: default init serve pytest bdd mut format lint sort run kik

default: bdd mut lint sort format

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
	poetry run python ./testing/bot.py

kik:
	python run python ./testing/kik_bot.py