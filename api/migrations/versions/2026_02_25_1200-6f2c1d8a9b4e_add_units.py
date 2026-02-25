"""Add units and unit_responsibles

Revision ID: 6f2c1d8a9b4e
Revises: 3d86e6fd9d2c
Create Date: 2026-02-25 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "6f2c1d8a9b4e"
down_revision: Union[str, None] = "3d86e6fd9d2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    level_enum = postgresql.ENUM(
        "View",
        "Edit",
        "Full",
        name="unit_responsible_level",
    )
    level_enum.create(op.get_bind(), checkfirst=True)
    level_enum_column = postgresql.ENUM(
        "View",
        "Edit",
        "Full",
        name="unit_responsible_level",
        create_type=False,
    )

    op.create_table(
        "units",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_units_id"), "units", ["id"], unique=False)
    op.create_index(op.f("ix_units_name"), "units", ["name"], unique=True)

    op.create_table(
        "unit_responsibles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("level", level_enum_column, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["unit_id"], ["units.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("unit_id", "user_id", name="uq_unit_responsibles_unit_user"),
    )
    op.create_index(op.f("ix_unit_responsibles_unit_id"), "unit_responsibles", ["unit_id"], unique=False)
    op.create_index(op.f("ix_unit_responsibles_user_id"), "unit_responsibles", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_unit_responsibles_user_id"), table_name="unit_responsibles")
    op.drop_index(op.f("ix_unit_responsibles_unit_id"), table_name="unit_responsibles")
    op.drop_table("unit_responsibles")
    op.drop_index(op.f("ix_units_name"), table_name="units")
    op.drop_index(op.f("ix_units_id"), table_name="units")
    op.drop_table("units")

    level_enum = postgresql.ENUM(
        "View",
        "Edit",
        "Full",
        name="unit_responsible_level",
    )
    level_enum.drop(op.get_bind(), checkfirst=True)
