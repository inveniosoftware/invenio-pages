# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def test_page_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    resp = base_client.get("/api/pages/1")
    assert resp.status_code == 200
    assert resp.json == {
        "title": "Page for Dogs!",
        "description": "",
        "url": "/dogs",
        "content": "Generic dog.",
        "id": "1",
        "links": {"self": "http://localhost/api/pages/1"},
    }


def test_html_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    resp = base_client.get("/api/pages/4")
    assert resp.status_code == 200
    assert resp.json == {
        "title": "Page for modern dogs!",
        "description": "",
        "url": "/htmldog",
        "content": "<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
        "id": "4",
        "links": {"self": "http://localhost/api/pages/4"},
    }


def test_page_etag(module_scoped_pages_fixture, base_client):
    """Test page content."""
    resp = base_client.get("/api/pages/1")
    assert resp.status_code == 200

    resp = base_client.get(
        "/api/pages/1", headers=(("If-None-Match", resp.headers.get("ETag")),)
    )
    assert resp.status_code == 304
