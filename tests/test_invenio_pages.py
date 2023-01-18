# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Module tests."""

from flask import Flask

from invenio_pages import InvenioPages


def test_version():
    """Test version import."""
    from invenio_pages import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    InvenioPages(app)
    assert "invenio-pages" in app.extensions

    app = Flask("testapp")
    ext = InvenioPages()
    assert "invenio-pages" not in app.extensions
    ext.init_app(app)
    assert "invenio-pages" in app.extensions
