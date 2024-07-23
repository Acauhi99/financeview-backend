"""add user_id to feedback

Revision ID: 79a74ad45c3c
Revises: dd421b655ddd
Create Date: 2024-07-22 18:42:05.315354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79a74ad45c3c'
down_revision: Union[str, None] = 'dd421b655ddd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Usando batch mode para a tabela feedback
    with op.batch_alter_table('feedback') as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_feedback_user_id', 'users', ['user_id'], ['id'])
    
    # Adicionando coluna url_image na tabela users
    op.add_column('users', sa.Column('url_image', sa.String(), nullable=True))


def downgrade() -> None:
    # Usando batch mode para a tabela feedback
    with op.batch_alter_table('feedback') as batch_op:
        batch_op.drop_constraint('fk_feedback_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # Removendo coluna url_image da tabela users
    op.drop_column('users', 'url_image')
