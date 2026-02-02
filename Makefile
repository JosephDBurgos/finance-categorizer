DOCKER_COMPOSE ?= docker-compose
APP_ENV ?= development

export APP_ENV

help:
	@echo "Available commands:"
	@echo "  make up         - Start all services in the background"
	@echo "  make down       - Stop and remove all services"
	@echo "  make logs       - Tail logs for the app and worker services"
	@echo "  make ps         - List the status of all services"
	@echo "  make restart    - Restart all services"
	@echo "  make rebuild    - Rebuild and start all services"
	@echo "  make db-seed    - Seed the database with initial data"
	@echo "  make migrate    - Apply database migrations using Alembic"
	@echo "  make cleanup    - Clean up all services, networks, and volumes"

up:
	@$(DOCKER_COMPOSE) up -d

down:
	@$(DOCKER_COMPOSE) down --remove-orphans

logs:
	@$(DOCKER_COMPOSE) logs -f app worker

ps:
	@$(DOCKER_COMPOSE) ps

restart: down up

rebuild:
	@$(DOCKER_COMPOSE) up --build -d

db-seed:
	@$(DOCKER_COMPOSE) --profile tools run --rm db-seed

migrate:
	@$(DOCKER_COMPOSE) run --rm app alembic upgrade head

cleanup:
	@$(DOCKER_COMPOSE) down --remove-orphans
	@$(DOCKER_COMPOSE) rm -f
	@docker volume rm finance-categorizer_postgres_data 2>/dev/null || true