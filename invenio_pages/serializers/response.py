# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module REST response serialisation."""

import json

from flask import current_app

from invenio_pages import Page


def page_responsify(schema_class, mimetype):
    """Create a page response serializer.

    :param serializer: Serializer instance.
    :param mimetype: MIME type of response.
    """

    def view(data, code=200, headers=None, links_item_factory=None):
        """Generate the response object."""
        if isinstance(data, Page):
            last_modified = data.updated
            response_data = schema_class(
                context=dict(item_links_factory=links_item_factory)
            ).dump(data)

        response = current_app.response_class(
            json.dumps(response_data), mimetype=mimetype
        )
        response.status_code = code

        if last_modified:
            response.last_modified = last_modified

        if headers is not None:
            response.headers.extend(headers)
        return response

    return view
