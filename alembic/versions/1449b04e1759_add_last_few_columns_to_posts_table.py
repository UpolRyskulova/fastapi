"""add last few columns to posts table

Revision ID: 1449b04e1759
Revises: c7c3448d16b1
Create Date: 2022-10-06 23:53:37.815484

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1449b04e1759'
down_revision = 'c7c3448d16b1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()')), )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
