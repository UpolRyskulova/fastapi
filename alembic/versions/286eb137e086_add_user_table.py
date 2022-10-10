"""add user table

Revision ID: 286eb137e086
Revises: 5d7acf18a13c
Create Date: 2022-10-06 23:42:16.863985

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '286eb137e086'
down_revision = '5d7acf18a13c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
