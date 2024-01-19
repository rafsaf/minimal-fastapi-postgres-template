#!/bin/bash

echo "Run migrations"
alembic upgrade head
