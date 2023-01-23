# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Results for the requests service."""

from flask_sqlalchemy import Pagination
from invenio_records_resources.services.records.results import RecordItem, RecordList


class PageItem(RecordItem):
    """Single page result."""

    def __init__(
        self,
        service,
        identity,
        page,
        links_tpl=None,
        errors=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(service, identity, page, errors, links_tpl, schema)

    @property
    def data(self):
        """Property to get the page."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._record,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data


class PageList(RecordList):
    """List of page results."""

    def __init__(
        self,
        service,
        identity,
        pages,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
        schema=None,
    ):
        """Constructor."""
        super().__init__(
            service, identity, pages, params, links_tpl, links_item_tpl, schema
        )

    @property
    def hits(self):
        """Iterator over the hits."""
        for record in self.pages_result():
            projection = self._schema.dump(
                record,
                context=dict(
                    identity=self._identity,
                    record=record,
                ),
            )

            if self._links_item_tpl:
                projection["links"] = self._links_item_tpl.expand(
                    self._identity, record
                )

            yield projection

    @property
    def total(self):
        """Get total number of pages."""
        return len(self.pages_result())

    def pages_result(self):
        """Gets the results, even if they are in a pagination object."""
        return (
            self._results.items if type(self._results) == Pagination else self._results
        )
