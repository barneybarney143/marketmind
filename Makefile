.PHONY: install lint test export

install:
	poetry install --with dev --no-interaction --no-root

lint:
	poetry run ruff check . && poetry run black --check .

test:
	poetry run pytest --cov=src --cov-fail-under=80

export:
	poetry export -f requirements.txt --without-hashes -o requirements.txt
