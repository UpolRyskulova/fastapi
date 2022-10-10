"""create post table

Revision ID: 846404acaf89
Revises: 
Create Date: 2022-10-06 23:25:53.362475

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '846404acaf89'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
