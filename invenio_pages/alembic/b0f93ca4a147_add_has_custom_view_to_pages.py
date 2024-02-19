#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Add has_custom_view to pages."""

import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b0f93ca4a147"
down_revision = "145402e8523a"
branch_labels = ()
depends_on = "98e0a418340d"


def upgrade():
    """Upgrade database."""
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


def downgrade():
    """Downgrade database."""
    # Drop the column
    op.drop_column("pages_page", "has_custom_view")
    op.drop_column("pages_page_version", "has_custom_view")
    # ### end Alembic commands ###
