"""Revised

Revision ID: ee5c421935ee
Revises: c57081dfbfec
Create Date: 2023-02-02 06:55:42.033793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee5c421935ee'
down_revision = 'c57081dfbfec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('work_start', sa.Integer(), nullable=False, default=9))
    op.add_column('user', sa.Column('work_end', sa.Integer(), nullable=False, default=20))
    op.add_column('user', sa.Column('rest_start', sa.Integer(), nullable=False, default=12))
    op.add_column('user', sa.Column('rest_end', sa.Integer(), nullable=False, default=13))


def downgrade() -> None:
    op.drop_column('user', 'work_start')
    op.drop_column('user', 'work_end')
    op.drop_column('user', 'rest_start')
    op.drop_column('user', 'rest_end')
