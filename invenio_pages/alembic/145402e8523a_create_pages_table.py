# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create pages table."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "145402e8523a"
down_revision = "98e0a418340d"
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    op.create_table(
        "pages_page",
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("url", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("description", sa.String(length=200), nullable=False),
        sa.Column("template_name", sa.String(length=70), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pages_page")),
        sa.UniqueConstraint("url", name=op.f("uq_pages_page_url")),
    )

    op.create_table(
        "pages_page_version",
        sa.Column("created", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("updated", sa.DateTime(), autoincrement=False, nullable=True),
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("url", sa.String(length=100), autoincrement=False, nullable=True),
        sa.Column("title", sa.String(length=200), autoincrement=False, nullable=True),
        sa.Column("content", sa.Text(), autoincrement=False, nullable=True),
        sa.Column(
            "description", sa.String(length=200), autoincrement=False, nullable=True
        ),
        sa.Column(
            "template_name", sa.String(length=70), autoincrement=False, nullable=True
        ),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_pages_page_version")
        ),
    )

    op.create_index(
        op.f("ix_pages_page_version_end_transaction_id"),
        "pages_page_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pages_page_version_operation_type"),
        "pages_page_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pages_page_version_transaction_id"),
        "pages_page_version",
        ["transaction_id"],
        unique=False,
    )

    op.create_table(
        "pages_pagelist_version",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("list_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("page_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column("order", sa.Integer(), autoincrement=False, nullable=True),
        sa.Column(
            "transaction_id", sa.BigInteger(), autoincrement=False, nullable=False
        ),
        sa.Column("end_transaction_id", sa.BigInteger(), nullable=True),
        sa.Column("operation_type", sa.SmallInteger(), nullable=False),
        sa.PrimaryKeyConstraint(
            "id", "transaction_id", name=op.f("pk_pages_pagelist_version")
        ),
    )
    op.create_index(
        op.f("ix_pages_pagelist_version_end_transaction_id"),
        "pages_pagelist_version",
        ["end_transaction_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pages_pagelist_version_operation_type"),
        "pages_pagelist_version",
        ["operation_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_pages_pagelist_version_transaction_id"),
        "pages_pagelist_version",
        ["transaction_id"],
        unique=False,
    )
    op.create_table(
        "pages_pagelist",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("list_id", sa.Integer(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["list_id"],
            ["pages_page.id"],
            name=op.f("fk_pages_pagelist_list_id_pages_page"),
        ),
        sa.ForeignKeyConstraint(
            ["page_id"],
            ["pages_page.id"],
            name=op.f("fk_pages_pagelist_page_id_pages_page"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_pages_pagelist")),
    )


def downgrade():
    """Downgrade database."""
    op.drop_table("pages_pagelist")
    op.drop_index(
        op.f("ix_pages_pagelist_version_transaction_id"),
        table_name="pages_pagelist_version",
    )
    op.drop_index(
        op.f("ix_pages_pagelist_version_operation_type"),
        table_name="pages_pagelist_version",
    )
    op.drop_index(
        op.f("ix_pages_pagelist_version_end_transaction_id"),
        table_name="pages_pagelist_version",
    )
    op.drop_table("pages_pagelist_version")
    op.drop_index(
        op.f("ix_pages_page_version_transaction_id"), table_name="pages_page_version"
    )
    op.drop_index(
        op.f("ix_pages_page_version_operation_type"), table_name="pages_page_version"
    )
    op.drop_index(
        op.f("ix_pages_page_version_end_transaction_id"),
        table_name="pages_page_version",
    )
    op.drop_table("pages_page_version")
    op.drop_table("pages_page")
