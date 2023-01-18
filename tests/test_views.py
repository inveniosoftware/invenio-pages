# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test views for Pages module."""

from unittest import mock

import pytest
from invenio_db import db
from jinja2.exceptions import UndefinedError
from werkzeug.exceptions import NotFound

from invenio_pages import Page
from invenio_pages.views import render_page


def test_page_content(pages_fixture, app, base_client):
    """Test page content."""

    resp = base_client.get("/dogs/shiba")
    assert resp.status_code == 200
    assert "so doge!" in str(resp.get_data())
    assert "so doge!" in str(render_page("/dogs/shiba"))


def test_page_content_dynamic(pages_fixture, app):
    """Test page content."""
    app.config["PAGES_WHITELIST_CONFIG_KEYS"] = ["MYVAR"]
    content = "dynamic-content"
    with app.app_context():
        app.config["MYVAR"] = content
        page = Page(
            url="/dynamic",
            title="Dynamic page",
            content="{{MYVAR}}",
            template_name="invenio_pages/dynamic.html",
        )
        db.session.add(page)
        db.session.commit()

        with app.test_request_context("/dynamic"):
            assert content in render_page("/dynamic")

        with app.test_client() as client:
            resp = client.get("/dynamic")
            assert resp.status_code == 200
            assert content in resp.get_data(as_text=True)


def test_current_app_and_config_not_visible(pages_fixture, app):
    """Test current_app and config are not visible to template."""
    app.config.update(SECRET_KEY="super secret")
    with app.app_context():
        page = Page(
            url="/dynamic",
            title="Dynamic page",
            content="{{SECRET_KEY}}",
            template_name="invenio_pages/dynamic.html",
        )
        db.session.add(page)
        db.session.commit()

        with app.test_request_context("/dynamic"):
            assert app.config["SECRET_KEY"] not in render_page("/dynamic")

            page.content = "{{config.SECRET_KEY}}"
            db.session.commit()
            with pytest.raises(UndefinedError):
                render_page("/dynamic")

            page.content = "{{current_app.config['SECRET_KEY']}}"
            db.session.commit()
            with pytest.raises(UndefinedError):
                render_page("/dynamic")


def test_non_existing_page(pages_fixture, app):
    """Test non-existing page content."""

    # render_page function
    with app.test_request_context("/invalid/url/errors"):
        with pytest.raises(NotFound):
            render_page("/invalid/url/errors")


def test_runtime_added_page(pages_fixture, app):
    """Test runtime added page."""

    with app.test_request_context("/runtime/added"):
        with app.test_client() as client:
            resp = client.get("/runtime/added")
            assert resp.status_code == 404

            new_page = Page(
                url="/runtime/added",
                title="Runtime added page!",
                content="added after initial page mapping.",
                template_name="invenio_pages/default.html",
            )
            db.session.add(new_page)
            db.session.commit()

            resp = client.get("/runtime/added")
            assert resp.status_code == 200
            assert "added after initial page mapping." in str(resp.get_data())


def test_pre_existing_404_function(pages_fixture, app):
    """Test pre existing 404."""
    with app.test_request_context("/runtime/added"):
        with app.test_client() as client:
            resp = client.get("/runtime/added")
            assert resp.status_code == 404

            new_page = Page(
                url="/runtime/added",
                title="Runtime added page!",
                content="added after initial page mapping.",
                template_name="invenio_pages/default.html",
            )
            db.session.add(new_page)
            db.session.commit()

            resp = client.get("/runtime/added")
            assert resp.status_code == 200
            assert "added after initial page mapping." in str(resp.get_data())
