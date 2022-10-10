"""add content column to posts table

Revision ID: 5d7acf18a13c
Revises: 846404acaf89
Create Date: 2022-10-06 23:29:37.190426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d7acf18a13c'
down_revision = '846404acaf89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
