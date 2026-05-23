# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Proxies for accessing the current Pages extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_pages = LocalProxy(lambda: current_app.extensions["invenio-pages"])
"""Proxy for the instantiated Pages extension."""

current_pages_service = LocalProxy(
    lambda: current_app.extensions["invenio-pages"].pages_service
)
"""Proxy for the currently instantiated pages service."""
