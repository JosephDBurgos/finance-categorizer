COMPOSE ?= docker compose
SERVICES ?= app worker postgres notifier

.PHONY: up down logs db-seed secrets ps restart migrate

up:
	$(COMPOSE) up -d $(SERVICES)

down:
	$(COMPOSE) down --remove-orphans

logs:
	$(COMPOSE) logs -f app worker

ps:
	$(COMPOSE) ps

restart: down up

db-seed:
	$(COMPOSE) run --rm db-seed

secrets:
	./scripts/mock-kms.sh init

migrate:
	alembic upgrade head
