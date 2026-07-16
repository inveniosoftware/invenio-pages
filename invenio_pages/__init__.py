# SPDX-FileCopyrightText: 2015-2025 CERN.
# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2025 KTH Royal Institute of Technology.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: MIT

"""Static pages module for Invenio."""

from .ext import InvenioPages, InvenioPagesREST
from .records.models import PageList, PageModel

__version__ = "10.0.2"

__all__ = ("__version__", "InvenioPages", "InvenioPagesREST", "PageModel", "PageList")
