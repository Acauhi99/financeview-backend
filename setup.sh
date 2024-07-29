set -e

pip install --upgrade pip
pip install -r requirements.txt

# if [ -f "test.db" ]; then
#     rm test.db
# fi

alembic upgrade head 