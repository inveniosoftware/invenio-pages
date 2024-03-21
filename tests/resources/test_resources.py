# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2024 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import pytest
from invenio_records_resources.services.errors import PermissionDeniedError

from invenio_pages.records.errors import PageNotCreatedError, PageNotFoundError


def test_page_content(module_scoped_pages_fixture, base_client):
    """Test page content."""
    page = base_client.get("/pages/1")
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
    page = base_client.get("/pages/4")
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
    pages = base_client.get("/pages")
    assert pages.status_code == 200
    assert pages.json["hits"]["total"] == 4

    pages = base_client.get("/pages?size=2")
    assert pages.json["hits"]["total"] == 2

    pages = base_client.get("/pages?sort=title")
    assert pages.json["hits"]["hits"][0]["id"] == "3"

    pages = base_client.get("/pages?sort=title&sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/pages?sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/pages?size=3&sort=title&sort_direction=desc")
    assert pages.json["hits"]["hits"][0]["id"] == "4"

    pages = base_client.get("/pages?sort=url")
    assert pages.json["hits"]["hits"][0]["id"] == "3"
    assert pages.json["hits"]["hits"][3]["id"] == "4"

    pages = base_client.get("/pages?q=Generic%20dog")
    assert pages.json["hits"]["total"] == 1

    pages = base_client.get("/pages?q=dog&sort_direction=desc")
    assert pages.json["hits"]["total"] == 3
    assert pages.json["hits"]["hits"][0]["id"] == "4"


def test_create(module_scoped_pages_fixture, client, superuser):
    data = {
        "url": "/astures",
        "title": "Astures",
        "content": "Astures",
        "description": "Los astures (astures en latín) fueron un grupo de pueblos celtas...",
        "template_name": "invenio_pages/default.html",
    }
    superuser.login(client)

    page = client.post("/pages", json=data)
    assert page.json["title"] == "Astures"
    assert page.status_code == 201

    id = page.json["id"]
    assert client.get(f"/pages/{id}").json["title"] == "Astures"

    with pytest.raises(PageNotCreatedError):
        client.post("/pages", json=data)


def test_delete(module_scoped_pages_fixture, client, superuser):
    data = {
        "url": "/cantabros",
        "title": "Cantabros",
        "content": "Cantabros",
        "description": "El término cántabros...",
        "template_name": "invenio_pages/default.html",
    }
    superuser.login(client)

    page = client.post("/pages", json=data)
    id = page.json["id"]
    assert client.get(f"/pages/{id}").json["title"] == "Cantabros"

    client.delete(f"/pages/{id}")
    with pytest.raises(PageNotFoundError):
        client.get(f"/pages/{id}").json["title"] == "Cantabros"


def test_update(module_scoped_pages_fixture, client, admin):
    data = {
        "url": "/lusitanos",
        "title": "Lusitanos",
        "content": "Lusitanos",
        "description": "El término lusitanos...",
    }
    admin.login(client)

    assert client.get("/pages/1").json["title"] != "Lusitanos"

    client.put("/pages/1", json=data)

    json = client.get("/pages/1").json
    assert json["title"] == "Lusitanos"
    assert json["template_name"] == "invenio_pages/default.html"


def test_update_denied(module_scoped_pages_fixture, client):
    data = {
        "url": "/lusitanos",
        "title": "Lusitanos",
        "content": "Lusitanos",
        "description": "El término lusitanos...",
    }
    with pytest.raises(PermissionDeniedError):
        client.put("/pages/1", json=data)


def test_create_denied(module_scoped_pages_fixture, client, admin):
    data = {
        "url": "/arevacos",
        "title": "Arévacos",
        "content": "Arévacos",
        "description": "Los término arévacos",
        "template_name": "invenio_pages/default.html",
    }
    admin.login(client)
    with pytest.raises(PermissionDeniedError):
        client.post("/pages", json=data)


def test_delete_denied(module_scoped_pages_fixture, client, admin, superuser):
    data = {
        "url": "/numantinos",
        "title": "Numantinos",
        "content": "Numantinos",
        "description": "El término numantinos...",
        "template_name": "invenio_pages/default.html",
    }
    superuser.login(client)
    page = client.post("/pages", json=data)
    superuser.logout(client)

    id = page.json["id"]
    admin.login(client)

    with pytest.raises(PermissionDeniedError):
        client.delete(f"/pages/{id}")
