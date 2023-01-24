# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service API."""

from invenio_records_resources.services import RecordService
from invenio_records_resources.services.base import LinksTemplate
from invenio_records_resources.services.base.utils import map_search_params
from invenio_records_resources.services.uow import unit_of_work
from sqlalchemy import func

from ..records.models import PageModel as Page


class PageService(RecordService):
    """Page Service."""

    @unit_of_work()
    def create(self, identity, data, uow=None):
        """Create a page."""
        self.require_permission(identity, "create")
        data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=False,
        )
        page = self.record_cls.create(data)

        response = self.result_item(
            self, identity, page, links_tpl=self.links_item_tpl, errors=errors
        )
        return response

    def read_by_url(self, identity, url):
        """Retrieve a page by url."""
        self.require_permission(identity, "read")
        page = self.record_cls.get_by_url(url)
        response = self.result_item(self, identity, page, links_tpl=self.links_item_tpl)
        return response

    def read(self, identity, id):
        """Retrieve a page."""
        self.require_permission(identity, "read")
        page = self.record_cls.get(id)
        response = self.result_item(self, identity, page, links_tpl=self.links_item_tpl)
        return response

    def search(self, identity, params={}):
        """Search for pages matching the querystring."""
        self.require_permission(identity, "search")

        search_params = map_search_params(self.config.search, params)
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

    @unit_of_work()
    def update(self, identity, data, id, uow=None):
        """Update a page."""
        self.require_permission(identity, "update")
        data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=False,
        )
        self.record_cls.update(data, id)
        page = self.record_cls.get(id)
        response = self.result_item(
            self, identity, page, links_tpl=self.links_item_tpl, errors=errors
        )
        return response

    @unit_of_work()
    def delete(self, identity, id, uow=None):
        """Delete a page."""
        self.require_permission(identity, "delete")
        page = self.record_cls.get(id)
        self.record_cls.delete(page)
        response = self.result_item(self, identity, page, links_tpl=self.links_item_tpl)
        return response

    @unit_of_work()
    def delete_all(self, identity, uow=None):
        """Delete all pages."""
        self.require_permission(identity, "delete")
        self.record_cls.delete_all()

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
