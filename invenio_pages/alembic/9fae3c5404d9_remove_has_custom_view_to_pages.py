# SPDX-FileCopyrightText: 2016-2024 CERN.
# SPDX-License-Identifier: MIT

"""Add has_custom_view to pages."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9fae3c5404d9"
down_revision = "b0f93ca4a147"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # Drop the column
    op.drop_column("pages_page", "has_custom_view")
    op.drop_column("pages_page_version", "has_custom_view")
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # Add the new column
    op.add_column(
        "pages_page",
        sa.Column(
            "has_custom_view",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.expression.literal(False),
            default=False,
        ),
    )
    op.add_column(
        "pages_page_version",
        sa.Column(
            "has_custom_view",
            sa.Boolean(),
            nullable=True,
            server_default=sa.sql.expression.literal(False),
            default=False,
        ),
    )
    # ### end Alembic commands ###
