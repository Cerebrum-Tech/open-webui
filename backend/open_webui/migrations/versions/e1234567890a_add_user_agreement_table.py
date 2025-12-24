"""Add user_agreement table for GDPR/EULA acceptance

Revision ID: e1234567890a
Revises: d31026856c01
Create Date: 2024-12-24 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "e1234567890a"
down_revision = "d31026856c01"
branch_labels = None
depends_on = None


def upgrade():
    # ### Create user_agreement table ###
    op.create_table(
        "user_agreement",
        sa.Column("id", sa.String(), primary_key=True),  # Same as user ID
        sa.Column("eula_accepted", sa.Boolean(), default=False, nullable=False),
        sa.Column("eula_accepted_at", sa.BigInteger(), nullable=True),
        sa.Column("gdpr_accepted", sa.Boolean(), default=False, nullable=False),
        sa.Column("gdpr_accepted_at", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    # ### Drop user_agreement table ###
    op.drop_table("user_agreement")

