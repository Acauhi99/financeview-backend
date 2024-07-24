"""Fix user_name column addition

Revision ID: 091bd0faacee
Revises: 0e145232ad2a
Create Date: 2024-07-24 01:30:47.484240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision: str = '091bd0faacee'
down_revision: Union[str, None] = '0e145232ad2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_table_columns(table_name: str) -> set:
    """Retorna um conjunto com os nomes das colunas da tabela especificada."""
    conn = op.get_bind()
    insp = reflection.Inspector.from_engine(conn)
    return set([col['name'] for col in insp.get_columns(table_name)])


def upgrade() -> None:
    conn = op.get_bind()
    columns = get_table_columns('feedback')
    
    if 'user_name' not in columns:
        op.add_column('feedback', sa.Column('user_name', sa.String(), nullable=False))
    
    if 'name' in columns:
        op.drop_column('feedback', 'name')


def downgrade() -> None:
    conn = op.get_bind()
    columns = get_table_columns('feedback')
    
    if 'name' not in columns:
        op.add_column('feedback', sa.Column('name', sa.String(), nullable=False))
    
    if 'user_name' in columns:
        op.drop_column('feedback', 'user_name')
