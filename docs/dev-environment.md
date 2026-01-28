# Development Environment

> **Purpose:** Document the local, zero-cost environment used for iterative development, demos, and portfolio evidence before moving to managed hosting.

## 1. Overview
- **Stack:** Docker Compose orchestrating `app`, `postgres`, `worker`, and optional `mailhog`/`notifier` services.
- **Goals:** Reproduce multi-tenant flows (ingest, categorize, review, audit) using synthetic data while exercising encryption contexts and access controls.
- **Cost Profile:** Runs entirely on developer workstation; no cloud dependencies required until ready for managed pilot.

## 2. Prerequisites
- Docker Engine ≥ 25.x and Docker Compose v2.
- Make (optional) for scripted workflows.
- `age` or `openssl` for local secret generation.
- Python or Node runtime (TBD) for helper CLIs/scripts.

## 3. Directory Structure (Local)
```
.
├── docker-compose.yml
├── app/                # API/CLI source
├── worker/             # async jobs (categorization, notifications)
├── db/seed/            # SQL migrations + seed fixtures
├── data/fixtures/      # Synthetic CSV/OFX samples (git-tracked)
├── data/local/         # User-specific imports (gitignored)
└── docs/
```

## 4. Services
| Service | Purpose | Notes |
| --- | --- | --- |
| `postgres` | Canonical transactional store with RLS enabled. | Initializes with migrations + sample workspaces/users. |
| `app` | API + CLI gateway exposing ingest/categorize endpoints. | Mounts source for hot reload. |
| `worker` | Background jobs (rule evaluation, review notifications). | Subscribes to queue (Redis/NATS TBD). |
| `notifier` (optional) | Captures emails/webhooks locally (e.g., MailHog). | Demonstrates review alerts. |

## 5. Configuration
- Base `.env.example` checked in; copy to `.env.local` with developer-specific secrets.
- Sensitive values (workspace mock KMS IDs, demo JWT secrets) generated via `make secrets` and stored in `.secrets/` (gitignored).
- Postgres volumes scoped per developer (`postgres_data_$USER`) to avoid collisions.

## 6. Sample Data Seeding
1. Run `docker compose up db-seed` (or `make db-seed`) to load:
   - Workspaces: `demo-household`, `demo-club` with admins/reviewers.
   - Accounts + ingest artifacts referencing synthetic CSVs under `data/fixtures/`.
   - Initial transactions, rules, overrides, and audit events aligning with documentation.
2. Re-run seed command with `RESET=1` to wipe and reload fixtures.

## 7. Key Workflows to Exercise
- **Ingest:** `docker compose run app cli ingest data/fixtures/bank1.csv --workspace demo-household`.
- **Categorize:** `cli categorize run --workspace demo-household --batch 2024-01` and inspect `transactions` table.
- **Review Queue:** `cli review list --workspace demo-club`, assign items, submit overrides, verify audit log entries.
- **Calibration:** Execute `cli categorize calibrate --workspace demo-household --batch-size 200` to simulate weight tuning.
- **Audit Export:** `cli audit export --workspace demo-household --format json` demonstrating tamper-evident chain.

## 8. Encryption Simulation
- Application-layer encryption uses `libsodium` or `age` with mock KMS key IDs stored in `workspace.encryption_key_ref`.
- Local helper `scripts/mock-kms.sh` decrypts/encrypts payloads; swap with real KMS client during managed pilot.

## 9. Troubleshooting & Observability
- Logs streamed via `docker compose logs -f app worker`.
- `localhost:8081` (pgAdmin or Adminer) optional for inspecting Postgres; protected behind local password.
- Health endpoint `http://localhost:8080/healthz` verifies migrations + seed status.

## 10. Portfolio Guidance
- Capture terminal recordings (asciinema) or screenshots showing ingest, review, calibration flows.
- Highlight in README that everything runs locally with synthetic data, reinforcing privacy and cost control.
- Note clear upgrade path: replace mock KMS + Docker Compose with managed Postgres + KMS when ready.

