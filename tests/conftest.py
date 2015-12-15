# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

from __future__ import absolute_import, print_function

import pytest
from flask import Flask
from flask_cli import FlaskCLI
from invenio_admin import InvenioAdmin
from invenio_db import InvenioDB, db

from invenio_pages import Page


@pytest.fixture
def app(request):
    """Flask application fixture."""
    app = Flask('testapp')
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI='sqlite://',
    )
    FlaskCLI(app)
    InvenioDB(app)
    with app.app_context():
        db.create_all()

    def teardown():
        with app.app_context():
            db.drop_all()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def admin_fixture(pages_fixture):

    def unprotected_factory(base_class):

        class UnprotectedAdminView(base_class):

            def is_accesible(self):
                return True

            def inaccessible_callback(self, name, **kwargs):
                pass

        return UnprotectedAdminView

    ext_admin = InvenioAdmin(
        pages_fixture,
        view_class_factory=unprotected_factory,
    )

    return pages_fixture


@pytest.fixture
def pages_fixture(app):
    with app.app_context():
        pages = [
            Page(
                url='/dogs',
                title='Page for Dogs!',
                content='Generic dog.',
                template_name='invenio_pages/default.html',
            ),
            Page(
                url='/dogs/shiba',
                title='Page for doge!',
                content='so doge!',
                template_name='invenio_pages/default.html',
            ),
            Page(
                url='/cows/',
                title='Page for Cows!',
                content='Generic cow.',
                template_name='invenio_pages/default.html',
            ),
        ]
        for page in pages:
            db.session.add(page)
        db.session.commit()

    return app
