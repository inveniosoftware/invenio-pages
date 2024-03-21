# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2024 CERN.
# Copyright (C) 2023 KTH Royal Institute of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import pytest
from flask import Flask, current_app
from invenio_records_resources.services.errors import PermissionDeniedError

from invenio_pages import InvenioPages
from invenio_pages.config import (
    PAGES_ALLOWED_EXTRA_HTML_ATTRS,
    PAGES_ALLOWED_EXTRA_HTML_TAGS,
)
from invenio_pages.proxies import current_pages_service
from invenio_pages.records.errors import PageNotCreatedError, PageNotFoundError
from invenio_pages.services.schemas import DynamicSanitizedHTML


def test_page_read(module_scoped_pages_fixture, simple_user_identity):
    """Test read service function."""
    page = current_pages_service.read(simple_user_identity, 1).data
    page.pop("created")
    page.pop("updated")
    expected_data = {
        "title": "Page for Dogs!",
        "description": "",
        "url": "/dogs",
        "content": "Generic dog.",
        "id": "1",
        "template_name": "invenio_pages/default.html",
        "links": {"self": "https://127.0.0.1:5000/api/pages/1"},
    }
    assert page == expected_data


def test_page_read_by_url(module_scoped_pages_fixture, simple_user_identity):
    """Test read_by_url service function."""
    page = current_pages_service.read_by_url(simple_user_identity, "/dogs").data
    page.pop("created")
    page.pop("updated")
    expected_data = {
        "title": "Page for Dogs!",
        "description": "",
        "url": "/dogs",
        "content": "Generic dog.",
        "id": "1",
        "template_name": "invenio_pages/default.html",
        "links": {"self": "https://127.0.0.1:5000/api/pages/1"},
    }
    assert page == expected_data


def test_search(module_scoped_pages_fixture, simple_user_identity):
    """Test search service function."""
    pages = current_pages_service.search(simple_user_identity)
    assert pages.total == 4

    pages = current_pages_service.search(simple_user_identity, {"size": 2})
    assert pages.total == 2

    pages = current_pages_service.search(simple_user_identity, {"sort": "title"})
    assert pages.to_dict()["hits"]["hits"][0]["id"] == "3"

    pages = current_pages_service.search(
        simple_user_identity, {"sort": "title", "sort_direction": "desc"}
    )
    assert pages.to_dict()["hits"]["hits"][0]["id"] == "4"

    pages = current_pages_service.search(
        simple_user_identity, {"sort_direction": "desc"}
    )

    assert pages.to_dict()["hits"]["hits"][0]["id"] == "4"

    pages = current_pages_service.search(
        simple_user_identity, {"size": 3, "sort": "title", "sort_direction": "desc"}
    )
    assert pages.to_dict()["hits"]["hits"][0]["id"] == "4"

    pages = current_pages_service.search(simple_user_identity, {"sort": "url"})
    assert pages.to_dict()["hits"]["hits"][0]["id"] == "3"
    assert pages.to_dict()["hits"]["hits"][3]["id"] == "4"

    pages = current_pages_service.search(simple_user_identity, {"q": "Generic dog"})
    assert pages.total == 1

    pages = current_pages_service.search(
        simple_user_identity, {"q": "dog", "sort_direction": "desc"}
    )
    assert pages.total == 3
    assert pages.to_dict()["hits"]["hits"][0]["id"] == "4"


def test_create(module_scoped_pages_fixture, superuser_identity):
    data = {
        "url": "/astures",
        "title": "Astures",
        "content": "Astures",
        "description": "Los astures (astures en latín) fueron un grupo de pueblos celtas...",
        "template_name": "invenio_pages/default.html",
    }
    page = current_pages_service.create(superuser_identity, data)
    assert page["title"] == "Astures"

    id = page["id"]
    assert current_pages_service.read(superuser_identity, id)["title"] == "Astures"

    with pytest.raises(PageNotCreatedError):
        current_pages_service.create(superuser_identity, data)


def test_delete(module_scoped_pages_fixture, superuser_identity):
    data = {
        "url": "/cantabros",
        "title": "Cantabros",
        "content": "Cantabros",
        "description": "El término cántabros...",
        "template_name": "invenio_pages/default.html",
    }
    page = current_pages_service.create(superuser_identity, data)
    id = page["id"]
    assert current_pages_service.read(superuser_identity, id)["title"] == "Cantabros"
    current_pages_service.delete(superuser_identity, page["id"])
    with pytest.raises(PageNotFoundError):
        current_pages_service.read(superuser_identity, id)


def test_update(module_scoped_pages_fixture, admin_user_identity):
    data = {
        "url": "/lusitanos",
        "title": "Lusitanos",
        "content": "Lusitanos",
        "description": "El término lusitanos...",
    }
    assert current_pages_service.read(admin_user_identity, 1)["title"] != "Lusitanos"
    current_pages_service.update(admin_user_identity, data, 1)

    page = current_pages_service.read(admin_user_identity, 1)
    assert page["title"] == "Lusitanos"
    assert page["template_name"] == "invenio_pages/default.html"


def test_update_denied(module_scoped_pages_fixture, simple_user_identity):
    data = {
        "url": "/lusitanos",
        "title": "Lusitanos",
        "content": "Lusitanos",
        "description": "El término lusitanos...",
    }
    with pytest.raises(PermissionDeniedError):
        current_pages_service.update(simple_user_identity, data, 1)


def test_create_denied(module_scoped_pages_fixture, admin_user_identity):
    data = {
        "url": "/arevacos",
        "title": "Arévacos",
        "content": "Arévacos",
        "description": "Los término arévacos",
        "template_name": "invenio_pages/default.html",
    }
    with pytest.raises(PermissionDeniedError):
        page = current_pages_service.create(admin_user_identity, data)


def test_delete_denied(
    module_scoped_pages_fixture, superuser_identity, admin_user_identity
):
    data = {
        "url": "/numantinos",
        "title": "Numantinos",
        "content": "Numantinos",
        "description": "El término numantinos...",
        "template_name": "invenio_pages/default.html",
    }
    page = current_pages_service.create(superuser_identity, data)
    with pytest.raises(PermissionDeniedError):
        current_pages_service.delete(admin_user_identity, page["id"])


def test_delete_all(module_scoped_pages_fixture, superuser_identity):
    current_pages_service.delete_all(superuser_identity)
    pages = current_pages_service.search(superuser_identity)
    assert pages.total == 0


def test_extra_allowed_html_tags():
    """Test instance folder loading."""
    app = Flask("testapp")
    InvenioPages(app)

    assert (
        app.config["PAGES_ALLOWED_EXTRA_HTML_ATTRS"] == PAGES_ALLOWED_EXTRA_HTML_ATTRS
    )
    assert app.config["PAGES_ALLOWED_EXTRA_HTML_TAGS"] == PAGES_ALLOWED_EXTRA_HTML_TAGS

    app.config["PAGES_ALLOWED_EXTRA_HTML_ATTRS"] = ["a"]
    app.config["PAGES_ALLOWED_EXTRA_HTML_TAGS"] = ["a"]
    InvenioPages(app)
    assert app.config["PAGES_ALLOWED_EXTRA_HTML_ATTRS"] == ["a"]
    assert app.config["PAGES_ALLOWED_EXTRA_HTML_TAGS"] == ["a"]


def test_dynamic_sanitized_html_initialization():
    """
    Test the initialization of the DynamicSanitizedHTML class.

    This test verifies that the default values for 'tags' and 'attrs'
    attributes of a DynamicSanitizedHTML instance are set to None.
    It asserts that both these attributes are None upon initialization,
    ensuring that the class starts with no predefined allowed tags or attributes.
    """
    html_sanitizer = DynamicSanitizedHTML()
    assert html_sanitizer.tags is None
    assert html_sanitizer.attrs is None


def test_dynamic_sanitized_html(app):
    """
    Tests DynamicSanitizedHTML with custom tags and attributes in an app context.
    Verifies if custom settings are properly applied and reflected in the output.
    """
    with app.app_context():
        # Set up the extra configuration
        current_app.config["PAGES_ALLOWED_EXTRA_HTML_TAGS"] = ["customtag"]
        current_app.config["PAGES_ALLOWED_EXTRA_HTML_ATTRS"] = {
            "customtag": ["data-custom"]
        }

        sanitizer = DynamicSanitizedHTML()
        sample_html = '<customtag data-custom="value">Test</customtag>'
        result = sanitizer._deserialize(sample_html, None, None)

        assert '<customtag data-custom="value">Test</customtag>' in result
