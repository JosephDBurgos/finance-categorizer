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

### Environment Configuration

1. Copy the example `.env` file to create your own `.env` file:
   ```sh
   cp .env.example .env
   ```

2. Update the values in the `.env` file as needed for your local setup.

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

## Project Setup

### Docker Compose Services

The application uses Docker Compose to manage the following services:

- **postgres**: PostgreSQL database for storing application data.
- **app**: The main application service (Python-based).
- **worker**: Background task processor (Python-based).
- **notifier**: MailHog service for testing email notifications.
- **db-seed**: A one-time service to populate the database with initial data.

### Makefile Commands

The `Makefile` provides shortcuts for common tasks:

- `make up`: Starts all services in the background.
- `make down`: Stops and removes all services.
- `make logs`: Tails logs for the `app` and `worker` services.
- `make ps`: Lists the status of all services.
- `make restart`: Restarts all services.
- `make db-seed`: Seeds the database with initial data.
- `make migrate`: Applies database migrations using Alembic.
- `make secrets`: Initializes secrets using the `mock-kms.sh` script.

## Environment Setup

This project uses `.env` files to manage environment-specific configurations. The `APP_ENV` variable determines which environment-specific `.env` file is loaded.

### Base `.env` File

Create a `.env` file in the root directory with the following content:

```env
APP_ENV=development
```

### Environment-Specific `.env` Files

Create the following files in the root directory:

- `.env.development`:
  ```env
  DATABASE_URL=postgresql://postgres:postgres@db:5432/finance_local
  DEBUG=True
  ```
- `.env.testing`:
  ```env
  DATABASE_URL=postgresql://postgres:postgres@db:5432/finance_test
  DEBUG=False
  ```
- `.env.production`:
  ```env
  DATABASE_URL=postgresql://prod_user:prod_password@prod_host:5432/prod_db
  DEBUG=False
  ```

### Switching Environments

Use the `Makefile` to switch environments:

```sh
make set-env APP_ENV=production
```

## Common Commands

- **Start Services**:
  ```sh
  make up
  ```
- **Stop Services**:
  ```sh
  make down
  ```
- **View Logs**:
  ```sh
  make logs
  ```
- **Run Migrations**:
  ```sh
  make migrate
  ```
- **Seed the Database**:
  ```sh
  make db-seed
  ```
