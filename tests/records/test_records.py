# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models for Pages module."""

from invenio_records_resources.services.base.utils import get_search_params

from invenio_pages import PageModel as Page
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


def test_search(module_scoped_pages_fixture, base_app):
    pages = Page.search(get_search_params(PageServiceConfig, {}))
    assert len(pages.items) == 4

    pages = Page.search(get_search_params(PageServiceConfig, {"size": 2}))
    assert len(pages.items) == 2

    pages = Page.search(get_search_params(PageServiceConfig, {"sort": "title"}))
    assert pages.items[0].id == 3

    pages = Page.search(
        get_search_params(
            PageServiceConfig, {"sort": "title", "sort_direction": "desc"}
        )
    )
    assert pages.items[0].id == 4

    pages = Page.search(
        get_search_params(PageServiceConfig, {"sort_direction": "desc"})
    )
    assert pages.items[0].id == 4

    pages = Page.search(
        get_search_params(
            PageServiceConfig, {"size": 3, "sort": "title", "sort_direction": "desc"}
        )
    )
    assert pages.items[0].id == 4

    pages = Page.search(get_search_params(PageServiceConfig, {"sort": "url"}))
    assert pages.items[0].id == 3
    assert pages.items[3].id == 4
