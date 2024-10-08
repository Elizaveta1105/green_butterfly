"""changes relation5

Revision ID: c85df02a0ef3
Revises: ff47b10f1017
Create Date: 2024-08-07 16:37:15.923684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c85df02a0ef3'
down_revision: Union[str, None] = 'ff47b10f1017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('images', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
