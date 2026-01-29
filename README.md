# finance-categorizer

Planning-first personal fintech backend for multi-tenant transaction ingestion, deterministic categorization, and audited review workflows.

## Documentation
- [docs/project-brief.md](docs/project-brief.md)
- [docs/data-model.md](docs/data-model.md)
- [docs/categorization.md](docs/categorization.md)
- [docs/threat-model.md](docs/threat-model.md)
- [docs/dev-environment.md](docs/dev-environment.md)

## Prerequisites
- Python 3.11+
- Docker Engine ≥ 25 + Docker Compose v2
- Make (optional but recommended)

## Setup
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local
```

Bring up the local stack and apply migrations/seed data:

```sh
make up
make migrate   # runs alembic upgrade head
make db-seed   # load placeholder fixtures (replace soon)
```

## Migrations
- Create new revision: `alembic revision -m "add example table"`
- Apply latest revision: `make migrate`

Alembic reads `DATABASE_URL` from `.env.local` (or environment) so host and container workflows stay aligned.

## Local Environment (WIP)
Use `docker-compose.yml` and the `Makefile` targets to spin up the placeholder stack:

```sh
make up        # start postgres/app/worker/notifier shells
make db-seed   # run placeholder seed script
make logs      # tail app/worker logs
```

See [docs/dev-environment.md](docs/dev-environment.md) for the full workflow, including sample data ingestion, rule evaluation, and mock KMS usage.
