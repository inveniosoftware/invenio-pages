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

    @property
    def hits(self):
        """Iterator over the hits."""
        for record in self._results:
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
        return len(self._results)

    @property
    def _results(self):
        return (
            self._page_results.items
            if isinstance(self._page_results, Pagination)
            else self._page_results
        )

    def to_dict(self):
        """Return result as a dictionary."""
        hits = list(self.hits)

        res = {
            "hits": {
                "hits": hits,
                "total": self.total,
            }
        }

        if self._params:
            if self._links_tpl:
                res["links"] = self._links_tpl.expand(self._identity, self.pagination)

        return res

    @_results.setter
    def _results(self, value):
        self._page_results = value
