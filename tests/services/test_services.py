# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_access.permissions import system_identity

from invenio_pages.proxies import current_pages_service


def test_page_read_id(module_scoped_pages_fixture):
    """Test read_id service function."""
    page = current_pages_service.read_id(1, system_identity).data
    page.pop("created")
    page.pop("updated")
    expected_data = {
        "title": "Page for Dogs!",
        "description": "",
        "url": "/dogs",
        "content": "Generic dog.",
        "id": "1",
        "links": {"self": "https://127.0.0.1:5000/api/pages/1"},
    }
    assert page == expected_data


def test_read_url(module_scoped_pages_fixture):
    """Test read_url service function."""
    page = current_pages_service.read_url("/dogs/shiba")
    assert page.__repr__() == "URL: /dogs/shiba, title: Page for doge!"
