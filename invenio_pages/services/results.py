# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Results for the requests service."""

from invenio_records_resources.services.records.results import RecordItem


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
        self._record = page
        self._identity = identity
        self._service = service
        self._data = None
        self._schema = schema or service.schema
        self._links_tpl = links_tpl
        self._errors = errors

    @property
    def id(self):
        """Identity of the page."""
        return self._record

    @property
    def links(self):
        """Get links for this result item."""
        return self._links_tpl.expand(self._identity, self._record)

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
