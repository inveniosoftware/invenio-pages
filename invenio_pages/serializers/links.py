# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio modules generate links factory."""

from flask import request, url_for


def default_links_item_factory(page):
    """Factory for record links generation."""
    return dict(
        self=url_for(".pages_item", page_id=page["id"], _external=True).format(
            protocol=request.environ["wsgi.url_scheme"],
            host=request.environ["HTTP_HOST"],
            page_id=page["id"],
        )
    )
