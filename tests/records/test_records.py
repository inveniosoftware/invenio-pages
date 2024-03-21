# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2024 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models for Pages module."""

import pytest
from invenio_records_resources.services.base.utils import map_search_params

from invenio_pages import PageModel as Page
from invenio_pages.records.errors import PageNotCreatedError, PageNotFoundError
from invenio_pages.services.config import PageServiceConfig


def test_page_repr(module_scoped_pages_fixture, base_app):
    dog_page = Page.get_by_url("/dogs/shiba")
    assert dog_page.__repr__() == "URL: /dogs/shiba, title: Page for doge!"


def test_page_versions(module_scoped_pages_fixture, base_app, db):
    dog_page = Page.get_by_url("/dogs")
    dog_page.title = "Just a dog!"
    db.session.commit()

    dog_page = Page.get_by_url("/dogs")
    assert "Just a dog!" == dog_page.title
    assert 2 == dog_page.versions.count()
    assert "Page for Dogs!" == dog_page.versions[0].title


def test_page_versions(module_scoped_pages_fixture, base_app, db):
    dog_page = Page.get_by_url("/dogs")
    dog_page.title = "Just a dog!"
    db.session.commit()

    dog_page = Page.get_by_url("/dogs")
    assert "Just a dog!" == dog_page.title
    assert 2 == dog_page.versions.count()
    assert "Page for Dogs!" == dog_page.versions[0].title


def test_read(module_scoped_pages_fixture, base_app):
    assert Page.get(1).title == "Page for Dogs!"
    with pytest.raises(PageNotFoundError):
        Page.get(10)


def test_search(module_scoped_pages_fixture, base_app):
    pages = Page.search(map_search_params(PageServiceConfig.search, {}), [])
    assert len(pages.items) == 4

    pages = Page.search(map_search_params(PageServiceConfig.search, {"size": 2}), [])
    assert len(pages.items) == 2

    pages = Page.search(
        map_search_params(PageServiceConfig.search, {"sort": "title"}), []
    )
    assert pages.items[0].id == 3

    pages = Page.search(
        map_search_params(
            PageServiceConfig.search,
            {"sort": "title", "sort_direction": "desc"},
        ),
        [],
    )
    assert pages.items[0].id == 4

    pages = Page.search(
        map_search_params(PageServiceConfig.search, {"sort_direction": "desc"}), []
    )
    assert pages.items[0].id == 4

    pages = Page.search(
        map_search_params(
            PageServiceConfig.search,
            {"size": 3, "sort": "title", "sort_direction": "desc"},
        ),
        [],
    )
    assert pages.items[0].id == 4

    pages = Page.search(
        map_search_params(PageServiceConfig.search, {"sort": "url"}), []
    )
    assert pages.items[0].id == 3
    assert pages.items[3].id == 4


def test_create(module_scoped_pages_fixture, base_app):
    data = {
        "url": "/astures",
        "title": "Astures",
        "content": "Astures",
        "description": "Los astures (astures en latín) fueron un grupo de pueblos celtas...",
        "template_name": "invenio_pages/default.html",
    }
    page = Page.create(data)
    assert page.title == "Astures"

    id = page.id
    assert Page.get(id).title == "Astures"

    with pytest.raises(PageNotCreatedError):
        Page.create(data)


def test_delete(module_scoped_pages_fixture, base_app):
    data = {
        "url": "/cantabros",
        "title": "Cantabros",
        "content": "Cantabros",
        "description": "El término cántabros...",
        "template_name": "invenio_pages/default.html",
    }
    page = Page.create(data)
    id = page.id
    assert Page.get(id).title == "Cantabros"
    Page.delete(page)
    with pytest.raises(PageNotFoundError):
        Page.get(id)


def test_update(module_scoped_pages_fixture, base_app):
    data = {
        "url": "/lusitanos",
        "title": "Lusitanos",
        "content": "Lusitanos",
        "description": "El término lusitanos...",
    }
    assert Page.get(1).title != "Lusitanos"
    Page.update(data, 1)
    page = Page.get(1)
    assert page.title == "Lusitanos"
    assert page.template_name == "invenio_pages/default.html"


def test_delete_all(module_scoped_pages_fixture, base_app):
    Page.delete_all()
    pages = Page.search(map_search_params(PageServiceConfig.search, {}), [])
    assert len(pages.items) == 0
