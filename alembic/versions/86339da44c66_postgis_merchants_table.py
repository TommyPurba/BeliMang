"""postgis + merchants table

Revision ID: 86339da44c66
Revises: 4fe0aeeb62f6
Create Date: 2025-09-30 00:09:39.890149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86339da44c66'
down_revision: Union[str, Sequence[str], None] = '4fe0aeeb62f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
