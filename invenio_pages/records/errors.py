# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors."""


class PageNotFoundError(Exception):
    """Page not found exception."""

    def __init__(self, identifier):
        """Constructor."""
        self.identifier = identifier

    @property
    def description(self):
        """Exception's description."""
        return f"The page identified by {self.identifier} cannot be found."


class PageNotCreatedError(Exception):
    """Page not created exception."""

    def __init__(self, url):
        """Constructor."""
        self.url = url

    @property
    def description(self):
        """Exception's description."""
        return f"The page with url {self.url} couldn't be created, likely due to a page with the same url already existing."
