# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
# Copyright (C) 2025 Northwestern University.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Page Service API."""

from .config import PageServiceConfig
from .results import PageItem
from .service import PageService

__all__ = (
    "PageService",
    "PageServiceConfig",
    "PageList",
    "PageItem",
)
