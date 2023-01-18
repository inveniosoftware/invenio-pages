# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio-pages module contains schemas and serializers."""
from .config import PageResourceConfig
from .resource import PageResource

__all__ = ("PageResource", "PageResourceConfig")
