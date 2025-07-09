#!/usr/bin/env bash
set -e

echo "Migrating database..."

if ! uv run alembic -c app/db/alembic.ini upgrade head; then
    echo "Database migration failed! Exiting container..."
    exit 1
fi

echo "Migrations deployed successfully!"

UVICORN_RELOAD_ARGS=""
if [ "$UVICORN_RELOAD_ENABLED" = "true" ]; then
  echo "Uvicorn will run with reload enabled."
  UVICORN_RELOAD_ARGS="--reload --reload-dir /opt/remnashop/app --reload-include *.ftl"
else
  echo "Uvicorn will run without reload."
fi

exec uv run uvicorn app.__main__:app --host "${APP_HOST}" --port "${APP_PORT}" ${UVICORN_RELOAD_ARGS}