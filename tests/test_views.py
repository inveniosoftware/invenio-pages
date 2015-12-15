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

"""Test views for Pages module."""

from __future__ import absolute_import, print_function

import pytest
from flask import current_app
from invenio_db import db
from werkzeug.exceptions import NotFound

from invenio_pages import InvenioPages, Page
from invenio_pages.views import blueprint, render_page


def test_page_content(pages_fixture):
    """Test page content."""
    app = pages_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        with app.test_client() as client:
            resp = client.get('/dogs/shiba')
            assert resp.status_code == 200
            assert 'so doge!' in str(resp.get_data())
            assert 'so doge!' in str(render_page('/dogs/shiba'))


def test_non_existing_page(pages_fixture):
    """Test non-existing page content."""
    app = pages_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    # render_page function
    with app.test_request_context('/invalid/url/errors'):
        with pytest.raises(NotFound):
            render_page('/invalid/url/errors')


def test_runtime_added_page(pages_fixture):
    """Test runtime added page."""
    app = pages_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.test_request_context('/runtime/added'):
        with app.test_client() as client:
            resp = client.get('/runtime/added')
            assert resp.status_code == 404

            new_page = Page(
                url='/runtime/added',
                title='Runtime added page!',
                content='added after initial page mapping.',
                template_name='invenio_pages/default.html',
            )
            db.session.add(new_page)
            db.session.commit()

            resp = client.get('/runtime/added')
            assert resp.status_code == 200
            assert 'added after initial page mapping.' in str(resp.get_data())


def test_pre_existing_404_function(pages_fixture):
    """Test pre existing 404."""
    app = pages_fixture

    app.existing_called = False

    def existing_handler(error):
        current_app.existing_called = True
        return error

    app.error_handler_spec[None][404] = existing_handler

    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.test_request_context('/runtime/added'):
        with app.test_client() as client:
            resp = client.get('/runtime/added')
            assert resp.status_code == 404
            assert app.existing_called

            new_page = Page(
                url='/runtime/added',
                title='Runtime added page!',
                content='added after initial page mapping.',
                template_name='invenio_pages/default.html',
            )
            db.session.add(new_page)
            db.session.commit()

            resp = client.get('/runtime/added')
            assert resp.status_code == 200
            assert 'added after initial page mapping.' in str(resp.get_data())
