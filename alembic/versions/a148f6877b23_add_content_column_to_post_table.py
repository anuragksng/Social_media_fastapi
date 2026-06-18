"""add content column to post table

Revision ID: a148f6877b23
Revises: a3c71e8d352a
Create Date: 2026-06-17 17:05:28.550206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a148f6877b23'
down_revision: Union[str, Sequence[str], None] = 'a3c71e8d352a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass
    

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
