#!/bin/bash
set -e

echo "Starting setup script"

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

echo "Cleaning database..."
rm test.db || { echo "Failed to clean database"; exit 1; }
echo "DB cleaned"

echo "Running alembic migrations..."
alembic upgrade head || { echo "Failed to run alembic migrations"; exit 1; }

echo "Setup script completed successfully"