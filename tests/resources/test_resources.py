# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def test_page_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    page = base_client.get("/api/pages/1")
    assert page.status_code == 200

    json = page.json
    json.pop("created")
    json.pop("updated")
    expected_data = {
        "title": "Page for Dogs!",
        "description": "",
        "url": "/dogs",
        "content": "Generic dog.",
        "id": "1",
        "template_name": "invenio_pages/default.html",
        "links": {"self": "https://127.0.0.1:5000/api/pages/1"},
    }
    assert json == expected_data


def test_html_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    page = base_client.get("/api/pages/4")
    assert page.status_code == 200

    json = page.json
    json.pop("created")
    json.pop("updated")
    expected_data = {
        "title": "Page for modern dogs!",
        "description": "",
        "url": "/htmldog",
        "content": "<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
        "id": "4",
        "template_name": "invenio_pages/default.html",
        "links": {"self": "https://127.0.0.1:5000/api/pages/4"},
    }
    assert json == expected_data


def test_search(module_scoped_pages_fixture, base_client):
    """Test search service function."""
    pages = base_client.get("/api/pages/")
    assert pages.status_code == 200
    assert pages.json["hits"]["total"] == 4

    pages = base_client.get("/api/pages/?size=2")
    assert pages.json["hits"]["total"] == 2

    pages = base_client.get("/api/pages/?sort=title")
    assert pages.json["hits"]["hits"][0]["id"] == "3"

    pages = base_client.get("/api/pages/?sort=title&sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/api/pages/?sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/api/pages/?size=3&sort=title&sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/api/pages/?sort=url")
    assert pages.json["hits"]["hits"][0]["id"] == "3"
    assert pages.json["hits"]["hits"][3]["id"] == "4"

    pages = base_client.get("/api/pages/?q=Generic%20dog")
    assert pages.json["hits"]["total"] == 1

    pages = base_client.get("/api/pages/?q=dog&sort_direction=desc")
    assert pages.json["hits"]["total"] == 3
    assert pages.json["hits"]["hits"][0]["id"] == "4"
