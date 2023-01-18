# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service API."""

from flask import abort
from invenio_access.permissions import system_identity
from invenio_records_resources.services import RecordService
from sqlalchemy.orm.exc import NoResultFound

from invenio_pages.records.models import PageModel as Page


class PageService(RecordService):
    """Page Service."""

    def read_url(self, url):
        """Retrieve a page."""
        return Page.get_by_url(url)

    def read_id(self, id, identity):
        """Retrieve a page."""
        self.require_permission(identity, "read")
        try:
            page = Page.get_by_id(id)
        except NoResultFound:
            abort(404)
        response = self.result_item(
            self, system_identity, page, links_tpl=self.links_item_tpl
        )
        return response
