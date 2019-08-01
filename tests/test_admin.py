# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test admin views for Pages module."""

from __future__ import absolute_import, print_function

import pytest
from wtforms.validators import ValidationError

from invenio_pages import InvenioPages, Page
from invenio_pages.admin import same_page_choosen, template_exists
from invenio_pages.views import blueprint


def test_template_exists(app):
    """Test field validator."""
    InvenioPages(app)
    app.register_blueprint(blueprint)

    class Field(object):
        def __init__(self, data):
            self.data = data

    with app.app_context():
        with pytest.raises(ValidationError):
            template_exists(None, Field('inexistent_template'))
        template_exists(None, Field('invenio_pages/base.html'))
        template_exists(None, Field('invenio_pages/default.html'))
        template_exists(None, Field('invenio_pages/edit.html'))


def test_same_page_choosen(app):
    """Test same page choosen."""
    def mock(attr, value):
        class Mock(object):
            pass
        setattr(Mock, attr, value)
        return Mock

    form = mock('_obj', mock('list_id', '1'))
    field = mock('data', mock('id', '1'))
    pytest.raises(ValidationError, same_page_choosen, form, field)


def test_pages_admin(admin_fixture):
    """Test field validator."""
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
            resp = client.get('/admin/page/new/')
            assert resp.status_code == 200
