"""Add account_domains and ns_accounts

Revision ID: 9a4f2c7d1e11
Revises: 6f2c1d8a9b4e
Create Date: 2026-02-25 22:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "9a4f2c7d1e11"
down_revision: Union[str, None] = "6f2c1d8a9b4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    account_domain_name_enum = postgresql.ENUM(
        "ukraine_host",
        "name_cheap",
        "go_daddy",
        "whois",
        "cloud_flare",
        name="account_domain_name",
    )
    account_domain_name_enum.create(op.get_bind(), checkfirst=True)
    account_domain_name_enum_column = postgresql.ENUM(
        "ukraine_host",
        "name_cheap",
        "go_daddy",
        "whois",
        "cloud_flare",
        name="account_domain_name",
        create_type=False,
    )

    account_domain_status_enum = postgresql.ENUM(
        "active",
        "inactive",
        "warning",
        "ban",
        name="account_domain_status",
    )
    account_domain_status_enum.create(op.get_bind(), checkfirst=True)
    account_domain_status_enum_column = postgresql.ENUM(
        "active",
        "inactive",
        "warning",
        "ban",
        name="account_domain_status",
        create_type=False,
    )

    op.create_table(
        "account_domains",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", account_domain_name_enum_column, nullable=False),
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=True),
        sa.Column("accesses", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", account_domain_status_enum_column, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_update_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["unit_id"], ["units.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "login", name="uq_account_domains_name_login"),
    )
    op.create_index(op.f("ix_account_domains_id"), "account_domains", ["id"], unique=False)
    op.create_index(op.f("ix_account_domains_login"), "account_domains", ["login"], unique=False)
    op.create_index(op.f("ix_account_domains_name"), "account_domains", ["name"], unique=False)
    op.create_index(op.f("ix_account_domains_status"), "account_domains", ["status"], unique=False)
    op.create_index(op.f("ix_account_domains_unit_id"), "account_domains", ["unit_id"], unique=False)

    op.create_table(
        "ns_accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("ns", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["account_domains.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_id", "ns", name="uq_ns_accounts_account_ns"),
    )
    op.create_index(op.f("ix_ns_accounts_account_id"), "ns_accounts", ["account_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_ns_accounts_account_id"), table_name="ns_accounts")
    op.drop_table("ns_accounts")

    op.drop_index(op.f("ix_account_domains_unit_id"), table_name="account_domains")
    op.drop_index(op.f("ix_account_domains_status"), table_name="account_domains")
    op.drop_index(op.f("ix_account_domains_name"), table_name="account_domains")
    op.drop_index(op.f("ix_account_domains_login"), table_name="account_domains")
    op.drop_index(op.f("ix_account_domains_id"), table_name="account_domains")
    op.drop_table("account_domains")

    account_domain_status_enum = postgresql.ENUM(
        "active",
        "inactive",
        "warning",
        "ban",
        name="account_domain_status",
    )
    account_domain_status_enum.drop(op.get_bind(), checkfirst=True)

    account_domain_name_enum = postgresql.ENUM(
        "ukraine_host",
        "name_cheap",
        "go_daddy",
        "whois",
        "cloud_flare",
        name="account_domain_name",
    )
    account_domain_name_enum.drop(op.get_bind(), checkfirst=True)

