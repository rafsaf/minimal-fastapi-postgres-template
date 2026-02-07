BIND_PORT ?= 8000
BIND_HOST ?= localhost

.PHONY: help
help:  ## Print this help message
	grep -E '^[\.a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.env:  ## Ensure there is env file or create one
	echo "No .env file found. Want to create it from .env.example? [y/n]" && read answer && if [ $${answer:-'N'} = 'y' ]; then cp .env.example .env;fi

.PHONY: local-setup
local-setup:  ## Setup local postgres database
	docker compose up -d

.PHONY: up
up: local-setup  ## Run FastAPI development server
	uv run alembic upgrade head
	uv run uvicorn app.main:app --reload --host $(BIND_HOST) --port $(BIND_PORT)

.PHONY: run
run: up  ## Alias for `up`

.PHONY: down
down:  ## Stop database
	docker compose down

.PHONY: test
test: local-setup  ## Run unit tests
	uv run pytest .

.PHONY: lint
lint: local-setup  ## Run all linters
	uv run pre-commit run -a
	uv run mypy .
