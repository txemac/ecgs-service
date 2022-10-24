"""new table user

Revision ID: 853ed0b84703
Revises: 497ff89af14d
Create Date: 2022-10-20 16:52:43.708268+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '853ed0b84703'
down_revision = '497ff89af14d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", UUID, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("role", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("user")
