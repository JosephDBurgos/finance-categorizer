# finance-categorizer

Planning-first personal fintech backend for multi-tenant transaction ingestion, deterministic categorization, and audited review workflows.

## Documentation
- [docs/project-brief.md](docs/project-brief.md)
- [docs/data-model.md](docs/data-model.md)
- [docs/categorization.md](docs/categorization.md)
- [docs/threat-model.md](docs/threat-model.md)
- [docs/dev-environment.md](docs/dev-environment.md)

## Local Environment (WIP)
Use `docker-compose.yml` and the `Makefile` targets to spin up the placeholder stack:

```sh
make up        # start postgres/app/worker/notifier shells
make db-seed   # run placeholder seed script
make logs      # tail app/worker logs
```

See [docs/dev-environment.md](docs/dev-environment.md) for the full workflow, including sample data ingestion, rule evaluation, and mock KMS usage.
