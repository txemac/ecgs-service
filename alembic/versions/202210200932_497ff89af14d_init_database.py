"""init database

Revision ID: 497ff89af14d
Revises:
Create Date: 2022-10-20 09:32:29.451561+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '497ff89af14d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ecg",
        sa.Column("id", UUID, nullable=False, index=True),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "channel",
        sa.Column("ecg_id", UUID, nullable=False, index=True),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("num_zero_crossing", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("ecg_id", "name"),
        sa.ForeignKeyConstraint(
            ["ecg_id"],
            ["ecg.id"],
        )
    )


def downgrade() -> None:
    op.drop_table("channel")
    op.drop_table("ecg")
