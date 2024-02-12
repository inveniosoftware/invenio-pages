# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# invenio-administration is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio administration pages view module."""
from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceEditView,
    AdminResourceListView,
)
from invenio_i18n import lazy_gettext as _


class PageListView(AdminResourceListView):
    """Configuration for pages list view."""

    api_endpoint = "/pages"
    name = "pages"
    resource_config = "pages_resource"
    search_request_headers = {"Accept": "application/json"}
    title = _("Pages")
    menu_label = _("Pages")
    category = _("Site management")
    pid_path = "id"
    icon = "file alternate outline"

    display_search = True
    display_delete = False
    display_create = False
    display_edit = True

    item_field_list = {
        "url": {"text": _("Url"), "order": 1, "width": 2},
        "title": {"text": _("Title"), "order": 2, "width": 3},
        "description": {"text": _("Description"), "order": 3, "width": 3},
        "created": {"text": _("Created"), "order": 4, "width": 3},
        "updated": {"text": _("Updated"), "order": 5, "width": 3},
    }

    search_config_name = "PAGES_SEARCH"
    search_facets_config_name = "PAGES_FACETS"
    search_sort_config_name = "PAGES_SORT_OPTIONS"


class PageEditView(AdminResourceEditView):
    """Configuration for page edit view."""

    name = "pages_edit"
    url = "/pages/<pid_value>/edit"
    resource_config = "pages_resource"
    pid_path = "id"
    api_endpoint = "/pages"
    title = _("Edit page")

    list_view_name = "pages"

    form_fields = {
        "created": {"order": 1},
        "updated": {"order": 2},
        "url": {
            "order": 3,
            "text": _("URL"),
            "description": _("Relative path to the page."),
        },
        "title": {
            "order": 4,
            "text": _("Title"),
            "description": _("Title of the page."),
        },
        "description": {
            "order": 5,
            "text": _("Description"),
            "description": _("Description of the page"),
        },
        "content": {
            "order": 6,
            "text": _("Content"),
            "description": _("Content displayed by the page."),
            "rows": 10,
        },
    }


class PageDetailView(AdminResourceDetailView):
    """Configuration for page detail view."""

    url = "/pages/<pid_value>"
    api_endpoint = "/pages"
    name = "page-details"
    resource_config = "pages_resource"
    title = _("Page")

    display_edit = True
    display_delete = False

    list_view_name = "pages"
    pid_path = "id"

    item_field_list = {
        "created": {"text": _("Created"), "order": 1},
        "updated": {"text": _("Updated"), "order": 2},
        "url": {"text": _("Url"), "order": 3},
        "title": {"text": _("Title"), "order": 4},
        "description": {"text": _("Description"), "order": 5},
        "content": {"text": _("Content"), "order": 6, "escape": True},
    }
