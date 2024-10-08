"""changed date format

Revision ID: 10d6b98c52e9
Revises: bbb88b22f32b
Create Date: 2024-07-20 17:53:04.570854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '10d6b98c52e9'
down_revision: Union[str, None] = 'bbb88b22f32b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spendings', sa.Column('date', sa.Date(), nullable=True))
    op.drop_column('spendings', 'data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('spendings', sa.Column('data', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('spendings', 'date')
    # ### end Alembic commands ###
