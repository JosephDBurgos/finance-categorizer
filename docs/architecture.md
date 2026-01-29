flowchart TB
  subgraph DockerCompose["Docker Compose Environment"]
    app["app\nPython 3.11\nCLI + API"]
    worker["worker\nPython 3.11\nBackground Jobs"]
    postgres["postgres\nCanonical DB\n(volume: postgres_data)"]
    notifier["notifier\nMailHog"]
    dbseed["db-seed\npsql seed.sql"]

    app -->|DATABASE_URL| postgres
    worker -->|DATABASE_URL| postgres
    dbseed --> postgres

    app --> notifier
    worker --> notifier
  end

  subgraph Migrations["Schema & Migrations"]
    alembic["Alembic\n(alembic.ini + env.py)\nupgrade head"]
  end

  alembic --> postgres
