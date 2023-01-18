# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page module config."""

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
