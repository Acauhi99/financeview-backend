set -e

pip install --upgrade pip
pip install -r requirements.txt

alembic upgrade head 