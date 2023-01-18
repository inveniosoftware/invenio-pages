# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module models serialisation schemas."""
import html

from marshmallow import Schema, fields, post_dump

from invenio_pages.serializers.links import default_links_item_factory


class PageSchemaV1(Schema):
    """Schema for a page."""

    id = fields.String()
    url = fields.String()
    title = fields.String()
    content = fields.String()
    description = fields.String()

    @post_dump
    def item_links_addition(self, data, **kwargs):
        """Add the links for each page."""
        links_item_factory = self.context.get(
            "links_item_factory", default_links_item_factory
        )
        data["links"] = links_item_factory(data)
        return data
