# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016, 2022 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


"""Pytest configuration."""
import pytest
from invenio_app.factory import create_app as _create_app

from invenio_pages import Page


@pytest.fixture(scope="module")
def app(base_app, database):
    """Invenio application with only database.

    Scope: module
    """
    yield base_app


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return _create_app


@pytest.fixture(scope="function")
def pages_fixture(app, db):
    """Page fixtures.

    Scope: function
    """
    pages = [
        Page(
            url="/dogs",
            title="Page for Dogs!",
            content="Generic dog.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/dogs/shiba",
            title="Page for doge!",
            content="so doge!",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/cows/",
            title="Page for Cows!",
            content="Generic cow.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/htmldog",
            title="Page for modern dogs!",
            content="<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
            template_name="invenio_pages/default.html",
        ),
    ]
    for page in pages:
        db.session.add(page)
    db.session.commit()


@pytest.fixture(scope="module")
def module_scoped_pages_fixture(app, database):
    """Page fixtures.

    Scope: module
    """
    db = database
    pages = [
        Page(
            url="/dogs",
            title="Page for Dogs!",
            content="Generic dog.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/dogs/shiba",
            title="Page for doge!",
            content="so doge!",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/cows/",
            title="Page for Cows!",
            content="Generic cow.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/htmldog",
            title="Page for modern dogs!",
            content="<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
            template_name="invenio_pages/default.html",
        ),
    ]
    for page in pages:
        db.session.add(page)
    db.session.commit()
