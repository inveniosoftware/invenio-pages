# SPDX-FileCopyrightText: 2015-2025 CERN.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2025-2026 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

"""Static pages module for Invenio."""

from .ext import InvenioPages, InvenioPagesREST
from .records.models import PageList, PageModel

__version__ = "9.1.1"

__all__ = ("__version__", "InvenioPages", "InvenioPagesREST", "PageModel", "PageList")
