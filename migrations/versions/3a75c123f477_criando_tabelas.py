"""criando tabelas

Revision ID: 3a75c123f477
Revises: 
Create Date: 2024-07-24 01:45:17.665337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a75c123f477'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('url_image', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True)
    )

    op.create_table('active_stocks',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column('ticker', sa.String(), unique=True, index=True)
    )

    op.create_table('feedback',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )


def downgrade():
    op.drop_table('feedback')
    op.drop_table('active_stocks')
    op.drop_table('users')