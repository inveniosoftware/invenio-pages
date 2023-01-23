# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_access.permissions import system_identity

from invenio_pages.proxies import current_pages_service


def test_page_read(module_scoped_pages_fixture):
    """Test read service function."""
    page = current_pages_service.read(1, system_identity).data
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


def test_page_read_url(module_scoped_pages_fixture):
    """Test read_url service function."""
    page = current_pages_service.read_url("/dogs", system_identity).data
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


def test_search(module_scoped_pages_fixture):
    """Test search service function."""
    pages = current_pages_service.search(system_identity)
    assert pages.total == 4

    pages = current_pages_service.search(system_identity, {"size": 2})
    assert pages.total == 2

    pages = current_pages_service.search(system_identity, {"sort": "title"})
    assert pages.pages_result()[0].id == 3

    pages = current_pages_service.search(
        system_identity, {"sort": "title", "sort_direction": "desc"}
    )
    assert pages.pages_result()[0].id == 4

    pages = current_pages_service.search(system_identity, {"sort_direction": "desc"})
    assert pages.pages_result()[0].id == 4

    pages = current_pages_service.search(
        system_identity, {"size": 3, "sort": "title", "sort_direction": "desc"}
    )
    assert pages.pages_result()[0].id == 4

    pages = current_pages_service.search(system_identity, {"sort": "url"})
    assert pages.pages_result()[0].id == 3
    assert pages.pages_result()[3].id == 4

    pages = current_pages_service.search(system_identity, {"q": "Generic dog"})
    assert pages.total == 1

    pages = current_pages_service.search(
        system_identity, {"q": "dog", "sort_direction": "desc"}
    )
    assert pages.total == 3
    assert pages.pages_result()[0].id == 4
