# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies for accessing the current Pages extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_pages = LocalProxy(lambda: current_app.extensions["invenio-pages"])
"""Proxy for the instantiated Pages extension."""

current_pages_service = LocalProxy(
    lambda: current_app.extensions["invenio-pages"].pages_service
)
"""Proxy for the currently instantiated pages service."""
