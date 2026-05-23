# SPDX-FileCopyrightText: 2015-2022 CERN.
# SPDX-License-Identifier: MIT
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
