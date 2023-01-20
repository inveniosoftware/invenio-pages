# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Static pages module for Invenio."""

from .ext import InvenioPages, InvenioPagesREST
from .models import Page, PageList

__version__ = "2.0.0a2"

__all__ = ("__version__", "InvenioPages", "InvenioPagesREST", "Page", "PageList")
