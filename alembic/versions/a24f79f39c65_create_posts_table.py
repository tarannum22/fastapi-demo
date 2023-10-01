"""create posts table

Revision ID: a24f79f39c65
Revises: 
Create Date: 2023-10-01 15:43:57.424046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a24f79f39c65'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
