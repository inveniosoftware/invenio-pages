# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service Configuration."""


from invenio_i18n import gettext as _
from invenio_records_resources.services import Link, RecordServiceConfig
from invenio_records_resources.services.records.links import pagination_links
from sqlalchemy import asc, desc

from ..records.models import PageModel
from .permissions import PagesPermissionPolicy
from .results import PageItem, PageList
from .schemas import PageSchema


class PagesLink(Link):
    """Link variables setter for Page links."""

    @staticmethod
    def vars(page, vars):
        """Variables for the URI template."""
        vars.update({"id": page.id})


class SearchOptions:
    """Search options."""

    sort_direction_default = "asc"
    sort_direction_options = {
        "asc": dict(
            title=_("Ascending"),
            fn=asc,
        ),
        "desc": dict(
            title=_("Descending"),
            fn=desc,
        ),
    }

    sort_default = "created"
    sort_options = {
        "id": dict(
            title=_("Id"),
            fields=["id"],
        ),
        "url": dict(
            title=_("Url"),
            fields=["url"],
        ),
        "title": dict(
            title=_("Title"),
            fields=["title"],
        ),
        "content": dict(
            title=_("Content"),
            fields=["content"],
        ),
        "template_name": dict(
            title=_("Template Name"),
            fields=["template_name"],
        ),
        "description": dict(
            title=_("Description"),
            fields=["description"],
        ),
        "created": dict(
            title=_("Created"),
            fields=["created"],
        ),
        "updated": dict(
            title=_("Updated"),
            fields=["updated"],
        ),
    }
    pagination_options = {
        "default_results_per_page": 25,
    }


class PageServiceConfig(RecordServiceConfig):
    """Service factory configuration."""

    permission_policy_cls = PagesPermissionPolicy
    schema = PageSchema
    search = SearchOptions
    result_item_cls = PageItem
    result_list_cls = PageList
    record_cls = PageModel
    links_item = {
        "self": PagesLink("{+api}/pages/{id}"),
    }
    links_search = pagination_links("{+api}/pages{?args*}")
