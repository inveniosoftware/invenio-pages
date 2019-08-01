# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models for Pages module."""

from __future__ import absolute_import, print_function

from invenio_db import db

from invenio_pages import InvenioPages, Page
from invenio_pages.views import blueprint


def test_page_repr(pages_fixture):
    app = pages_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        dog_page = Page.get_by_url('/dogs/shiba')
        assert dog_page.__repr__() == 'URL: /dogs/shiba, title: Page for doge!'


def test_page_versions(pages_fixture):
    app = pages_fixture
    InvenioPages(app)
    app.register_blueprint(blueprint)

    with app.app_context():
        dog_page = Page.get_by_url('/dogs')
        dog_page.title = 'Just a dog!'
        db.session.commit()

    with app.app_context():
        dog_page = Page.get_by_url('/dogs')
        assert 'Just a dog!' == dog_page.title
        assert 2 == dog_page.versions.count()
        assert 'Page for Dogs!' == dog_page.versions[0].title
