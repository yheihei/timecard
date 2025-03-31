# Getting Started

```
docker compose build
docker compose up -d
docker compose run --entrypoint="" app poetry run python -m api.migrate_db
```

# How to test

```
# TODO: entrypoint上書きしないようにする
docker compose run --entrypoint="" app poetry run pytest -s -p no:warnings -v
```
