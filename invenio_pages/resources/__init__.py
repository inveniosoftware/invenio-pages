# SPDX-FileCopyrightText: 2015-2022 CERN.
# SPDX-License-Identifier: MIT

"""Invenio-pages module contains schemas and serializers."""

from .config import PageResourceConfig
from .resource import PageResource

__all__ = ("PageResource", "PageResourceConfig")
