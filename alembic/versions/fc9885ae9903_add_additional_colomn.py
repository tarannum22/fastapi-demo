"""add additional colomn

Revision ID: fc9885ae9903
Revises: a24f79f39c65
Create Date: 2023-10-01 16:58:11.330303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc9885ae9903'
down_revision: Union[str, None] = 'a24f79f39c65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=True))
    pass

def downgrade() -> None:
    op.drop_column('posts','content')
    pass
