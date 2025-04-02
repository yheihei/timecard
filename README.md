# Getting Started

## Start Container

```
docker compose build
docker compose up -d
```

# Migration

```
docker compose run app bash
# python -m api.migrate_db

or

docker compose run app poetry poe migrate
```

# How to test

```
docker compose run app bash
# pytest -s -p no:warnings -v

or

docker compose run app poetry poe test
```

# Formatter and check tool

```
docker compose run app poetry poe autoflake
docker compose run app poetry poe isort
docker compose run app poetry poe mypy
```
