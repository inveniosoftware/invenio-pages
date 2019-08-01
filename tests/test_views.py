# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test views for Pages module."""

from __future__ import absolute_import, print_function

import pytest
from flask import current_app
from invenio_db import db
from jinja2.exceptions import UndefinedError
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


def test_page_content_dynamic(app):
    """Test page content."""
    app.config['PAGES_WHITELIST_CONFIG_KEYS'] = ['MYVAR']
    InvenioPages(app)
    app.register_blueprint(blueprint)
    content = 'dynamic-content'
    with app.app_context():
        app.config['MYVAR'] = content
        page = Page(
            url='/dynamic',
            title='Dynamic page',
            content='{{MYVAR}}',
            template_name='invenio_pages/dynamic.html',
        )
        db.session.add(page)
        db.session.commit()

        with app.test_request_context('/dynamic'):
            assert content in render_page('/dynamic')

        with app.test_client() as client:
            resp = client.get('/dynamic')
            assert resp.status_code == 200
            assert content in resp.get_data(as_text=True)


def test_current_app_and_config_not_visible(app):
    """Test current_app and config are not visible to template."""
    app.config.update(
        SECRET_KEY='super secret'
    )
    InvenioPages(app)
    app.register_blueprint(blueprint)
    with app.app_context():
        page = Page(
            url='/dynamic',
            title='Dynamic page',
            content="{{SECRET_KEY}}",
            template_name='invenio_pages/dynamic.html',
        )
        db.session.add(page)
        db.session.commit()

        with app.test_request_context('/dynamic'):
            assert app.config['SECRET_KEY'] not in render_page('/dynamic')

            page.content = '{{config.SECRET_KEY}}'
            db.session.commit()
            with pytest.raises(UndefinedError):
                render_page('/dynamic')

            page.content = "{{current_app.config['SECRET_KEY']}}"
            db.session.commit()
            with pytest.raises(UndefinedError):
                render_page('/dynamic')


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

    app.register_error_handler(404, existing_handler)

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
