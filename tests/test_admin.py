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

"""Test admin views for Pages module."""

from __future__ import absolute_import, print_function

import pytest
from flask import url_for
from invenio_db import db
from wtforms.validators import ValidationError

from invenio_pages import InvenioPages, Page
from invenio_pages.admin import template_exists
from invenio_pages.views import blueprint


def test_template_exists(app):
    InvenioPages(app)
    app.register_blueprint(blueprint)

    class Field():

        def __init__(self, data):
            self.data = data

    with app.app_context():
        with pytest.raises(ValidationError):
            template_exists(None, Field('inexistent_template'))
        template_exists(None, Field('base.html'))
        template_exists(None, Field('default.html'))
        template_exists(None, Field('default_base.html'))
        template_exists(None, Field('edit.html'))
        template_exists(None, Field('edit_base.html'))


def test_pages_admin(admin_fixture):
    app = admin_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.test_request_context():
        with app.test_client() as client:
            resp = client.get('/admin/page/')
            assert resp.status_code == 200
            for page in Page.query.all():
                assert page.url in str(resp.get_data())
                assert page.title in str(resp.get_data())
