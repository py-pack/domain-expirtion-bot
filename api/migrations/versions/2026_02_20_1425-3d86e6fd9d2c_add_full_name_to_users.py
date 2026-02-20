"""Add full_name to users

Revision ID: 3d86e6fd9d2c
Revises: bb9e8f174dd0
Create Date: 2026-02-20 14:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "3d86e6fd9d2c"
down_revision: Union[str, None] = "bb9e8f174dd0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("full_name", sa.String(length=255), nullable=False, server_default=""),
    )
    op.add_column(
        "users",
        sa.Column(
            "settings",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
    )
    op.alter_column("users", "full_name", server_default=None)
    op.alter_column("users", "settings", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "settings")
    op.drop_column("users", "full_name")
