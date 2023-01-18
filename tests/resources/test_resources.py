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
        "links": {"self": "https://127.0.0.1:5000/api/pages/1"},
    }
    assert json == expected_data


def test_html_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    page = base_client.get("/api/pages/4")

    json = page.json
    json.pop("created")
    json.pop("updated")
    expected_data = {
        "title": "Page for modern dogs!",
        "description": "",
        "url": "/htmldog",
        "content": "<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
        "id": "4",
        "links": {"self": "https://127.0.0.1:5000/api/pages/4"},
    }
    assert json == expected_data
