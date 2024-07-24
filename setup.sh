set -e

echo "Starting setup script"

echo "Installing dependencies..."
pip install -r requirements.txt || { echo "Failed to install dependencies"; exit 1; }

echo "Running alembic migrations..."
alembic upgrade head || { echo "Failed to run alembic migrations"; exit 1; }

echo "Setup script completed successfully"