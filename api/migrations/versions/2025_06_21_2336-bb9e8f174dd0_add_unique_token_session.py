"""Add unique token session

Revision ID: bb9e8f174dd0
Revises: 759d6b517637
Create Date: 2025-06-21 23:36:57.308970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'bb9e8f174dd0'
down_revision: Union[str, None] = '759d6b517637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('refresh_tokens', sa.Column('session_id', sa.UUID(), nullable=False))
    op.add_column('refresh_tokens', sa.Column('user_agent', sa.String(), nullable=True))
    op.create_index(op.f('ix_refresh_tokens_session_id'), 'refresh_tokens', ['session_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_refresh_tokens_session_id'), table_name='refresh_tokens')
    op.drop_column('refresh_tokens', 'user_agent')
    op.drop_column('refresh_tokens', 'session_id')
