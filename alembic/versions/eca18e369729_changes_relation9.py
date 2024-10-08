"""changes relation9

Revision ID: eca18e369729
Revises: f69bbc92934a
Create Date: 2024-08-07 17:00:29.360929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eca18e369729'
down_revision: Union[str, None] = 'f69bbc92934a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('section', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('spendings', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('spendings', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('section', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('images', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
