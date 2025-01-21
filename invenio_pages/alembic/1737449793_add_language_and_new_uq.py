#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
# Copyright (C) 2025 University of Münster.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Add language and new uq"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1737449793"
down_revision = "9fae3c5404d9"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # Add new column and replace unique constraint
    op.add_column(
        "pages_page",
        sa.Column(
            "lang",
            sa.VARCHAR(length=2),
            server_default=sa.text("'en'::character varying"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(op.f("uq_pages_page_url"), "pages_page", type_="unique")
    op.create_unique_constraint("uq_pages_page_url_lang", "pages_page", ["url", "lang"])
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # Remove lang column and unique constraint
    op.drop_constraint("uq_pages_page_url_lang", "pages_page", type_="unique")
    op.create_unique_constraint(op.f("uq_pages_page_url"), "pages_page", ["url"])
    op.drop_column("pages_page", "lang")
    # ### end Alembic commands ###
