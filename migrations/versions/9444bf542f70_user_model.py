"""User model

Revision ID: 9444bf542f70
Revises: e8b5f9e26eb4
Create Date: 2024-04-28 12:29:59.808785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9444bf542f70'
down_revision: Union[str, None] = 'e8b5f9e26eb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
