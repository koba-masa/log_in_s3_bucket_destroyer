.PHONY: install, run, lint, fix, test, ci, metrics

install:
	docker-compose run --rm app poetry install

lint:
	docker-compose run --rm app poetry run mypy --explicit-package-bases .
	docker-compose run --rm app poetry run ruff check .
	docker-compose run --rm app poetry run black --check .

fix:
	docker-compose run --rm app poetry run ruff check . --fix-only --exit-zero
	docker-compose run --rm app poetry run black .

test:
	docker-compose run --rm app poetry run pytest -s

ci:
	make lint
	make test

