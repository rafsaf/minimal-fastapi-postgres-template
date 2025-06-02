#!/bin/bash
set -e

echo "Run migrations"
alembic upgrade head

# Run whatever CMD was passed
exec "$@"