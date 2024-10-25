.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  ref		Reformat code"
	@echo "  run		Start the app"
	@echo "  migrate	Alembic migrate database"
	@echo "  generate	Alembic generate database"
	@echo "  req		pyproject.toml >> requirements.txt"


.PHONY: ref
ref: poetry run pre-commit run --all-files

.PHONY: run
run:
	set -a; source .env; set +a; \
	poetry run python -m app.main

.PHONY: migrate
migrate:
	set -a; source .env; set +a; \
	poetry run alembic upgrade head

.PHONY: generate
generate:
	set -a; source .env; set +a; \
	poetry run alembic revision --autogenerate

.PHONY: req
req:
	@poetry export --without-hashes --without-urls | sed 's/;.*//' | tee requirements.txt