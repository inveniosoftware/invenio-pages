# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service Configuration."""


from invenio_records_resources.services import Link, RecordServiceConfig

from ..records.models import PageModel
from .permissions import PagesPermissionPolicy
from .results import PageItem
from .schemas import PageSchema


class PagesLink(Link):
    """Link variables setter for Page links."""

    @staticmethod
    def vars(page, vars):
        """Variables for the URI template."""
        vars.update({"id": page.id})


class PageServiceConfig(RecordServiceConfig):
    """Service factory configuration."""

    permission_policy_cls = PagesPermissionPolicy
    schema = PageSchema
    result_item_cls = PageItem
    record_cls = PageModel

    links_item = {
        "self": PagesLink("{+api}/pages/{id}"),
    }
