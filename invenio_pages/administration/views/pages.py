# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# invenio-administration is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio administration pages view module."""
from flask_babelex import lazy_gettext as _
from invenio_administration.views.base import (
    AdminResourceDetailView,
    AdminResourceEditView,
    AdminResourceListView,
)


class PageListView(AdminResourceListView):
    """Configuration for pages list view."""

    api_endpoint = "/pages"
    name = "Pages"
    resource_config = "pages_resource"
    search_request_headers = {"Accept": "application/json"}
    title = "Pages"
    category = "Pages"
    pid_path = "id"
    icon = "file alternate outline"
    template = "invenio_pages/administration/page_search.html"

    display_search = True
    display_delete = False
    display_create = False
    display_edit = True

    item_field_list = {
        "url": {"text": _("Url"), "order": 1},
        "title": {"text": _("Title"), "order": 2},
        "content": {"text": _("Content"), "order": 3},
        "template_name": {"text": _("Template Name"), "order": 4},
        "description": {"text": _("Description"), "order": 5},
        "created": {"text": _("Created"), "order": 6},
        "updated": {"text": _("Updated"), "order": 7},
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
    title = "Edit Page set"

    list_view_name = "Pages"

    form_fields = {
        "url": {
            "order": 1,
            "text": _("URL"),
            "description": _("Relative path to the page."),
        },
        "title": {
            "order": 2,
            "text": _("Title"),
            "description": _("Title of the page."),
        },
        "content": {
            "order": 3,
            "text": _("Content"),
            "description": _("Content displayed by the page."),
        },
        "template_name": {
            "order": 4,
            "text": _("Template name"),
            "description": _("Jinja template used to display the page."),
        },
        "description": {
            "order": 5,
            "text": _("Description"),
            "description": _("Description of the page"),
        },
        "created": {"order": 6},
        "updated": {"order": 7},
    }


class PageDetailView(AdminResourceDetailView):
    """Configuration for page detail view."""

    url = "/pages/<pid_value>"
    api_endpoint = "/pages"
    name = "page-details"
    resource_config = "pages_resource"
    title = "Page"

    template = "invenio_pages/administration/page_details.html"
    display_edit = True
    display_delete = False

    list_view_name = "Pages"
    pid_path = "id"

    item_field_list = {
        "id": {"text": _("Id"), "order": 1},
        "url": {"text": _("Url"), "order": 2},
        "title": {"text": _("Title"), "order": 3},
        "content": {"text": _("Content"), "order": 4},
        "template_name": {"text": _("Template Name"), "order": 5},
        "description": {"text": _("Description"), "order": 6},
        "created": {"text": _("Created"), "order": 7},
        "updated": {"text": _("Updated"), "order": 8},
    }
