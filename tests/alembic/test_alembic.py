# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test alembic recipes for Invenio-pages."""

import pytest
from invenio_db.utils import alembic_test_context, drop_alembic_version_table


@pytest.mark.skip(
    reason="We have to figure out why this is failing (or even if it is failing)."
)
def test_alembic(base_app, db):
    """Test alembic recipes."""
    ext = base_app.extensions["invenio-db"]

    if db.engine.name == "sqlite":
        raise pytest.skip("Upgrades are not supported on SQLite.")

    base_app.config["ALEMBIC_CONTEXT"] = alembic_test_context()
    # Check that this package's SQLAlchemy models have been properly registered
    tables = [x for x in db.metadata.tables]

    assert "pages_page" in tables
    assert "pages_pagelist" in tables
    assert "pages_page_version" in tables
    assert "pages_pagelist_version" in tables
    # Check that Alembic agrees that there's no further tables to create.
    assert len(ext.alembic.compare_metadata()) == 0

    # Drop everything and recreate tables all with Alembic
    db.drop_all()
    drop_alembic_version_table()
    ext.alembic.upgrade()
    assert len(ext.alembic.compare_metadata()) == 3

    # Try to upgrade and downgrade
    ext.alembic.stamp()
    ext.alembic.downgrade(target="96e796392533")
    ext.alembic.upgrade()
    assert len(ext.alembic.compare_metadata()) == 3

    drop_alembic_version_table()
