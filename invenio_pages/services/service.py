# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service API."""

from invenio_access.permissions import system_identity
from invenio_records_resources.services import RecordService
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import get_search_params
from sqlalchemy import func

from ..records.models import PageModel as Page


class PageService(RecordService):
    """Page Service."""

    def read_url(self, url, identity):
        """Retrieve a page."""
        self.require_permission(identity, "read")
        page = self.record_cls.get_by_url(url)
        response = self.result_item(
            self, system_identity, page, links_tpl=self.links_item_tpl
        )
        return response

    def read(self, id, identity):
        """Retrieve a page."""
        self.require_permission(identity, "read")
        page = self.record_cls.get(id)
        response = self.result_item(
            self, system_identity, page, links_tpl=self.links_item_tpl
        )
        return response

    def search(self, identity, params={}):
        """Search for pages matching the querystring."""
        self.require_permission(identity, "search")

        search_params = get_search_params(self.config, params)
        query = search_params["q"]
        filters = []

        if query:
            self._query_filters(filters, query)

        pages = self.record_cls.search(search_params, filters)
        return self.result_list(
            self,
            identity,
            pages,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def _query_filters(self, filters, query):
        filters.extend(
            [
                Page.url.ilike(f"%{query}%"),
                Page.title.ilike(f"%{query}%"),
                Page.content.ilike(f"%{query}%"),
                Page.description.ilike(f"%{query}%"),
                Page.template_name.ilike(f"%{query}%"),
            ]
        )
        datetime_value = self._validate_datetime(query)
        if datetime_value is not None:
            filters.extend(
                [
                    func.date(Page.created) == datetime_value,
                    func.date(Page.updated) == datetime_value,
                ]
            )

    def _validate_datetime(self, value):
        from datetime import datetime

        try:
            datetime_value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None
        return datetime_value
