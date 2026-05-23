# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-FileCopyrightText: 2025 Northwestern University.
# SPDX-License-Identifier: MIT

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
