.PHONY: default init bdd test format sort lint

default: test format sort lint

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
