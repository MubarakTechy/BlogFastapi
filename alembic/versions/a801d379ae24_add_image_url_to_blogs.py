"""add image_url to blogs

Revision ID: a801d379ae24
Revises: e68fa9da9fd5
Create Date: 2026-08-26 05:31:47.481680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a801d379ae24'
down_revision: Union[str, Sequence[str], None] = 'e68fa9da9fd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column(
        "blogs",
        sa.Column("image_url", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("blogs", "image_url")
