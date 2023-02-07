# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page module config."""

from flask_babelex import lazy_gettext as _

PAGES_DEFAULT_TEMPLATE = "invenio_pages/default.html"
"""Default template to render."""

PAGES_TEMPLATES = [
    ("invenio_pages/default.html", "Default"),
    ("invenio_pages/dynamic.html", "Default dynamic"),
]
"""List of available templates for pages."""

PAGES_WHITELIST_CONFIG_KEYS = [
    "THEME_SITENAME",
]
"""List of configuration variables accessible in the dynamic pages."""

PAGES_SEARCH = {
    "facets": [],
    "sort": ["url", "title", "created", "updated"],
}
"""Community search configuration (i.e list of communities)"""

PAGES_SORT_OPTIONS = {
    "url": dict(
        title=_("URL"),
        fields=["url"],
    ),
    "title": dict(
        title=_("Title"),
        fields=["title"],
    ),
    "created": dict(
        title=_("Created"),
        fields=["created"],
    ),
    "updated": dict(
        title=_("Updated"),
        fields=["updated"],
    ),
}
"""Definitions of available record sort options."""

PAGE_FACETS = {}
"""Available facets defined for this module."""
