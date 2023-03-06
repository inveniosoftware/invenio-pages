# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors."""

from invenio_i18n import gettext as _


class PageNotFoundError(Exception):
    """Page not found exception."""

    def __init__(self, identifier):
        """Initialise error."""
        super().__init__(
            _(
                "The page identified by {identifier} cannot be found.".format(
                    identifier=identifier
                )
            )
        )


class PageNotCreatedError(Exception):
    """Page not created exception."""

    def __init__(self, url):
        """Initialise error."""
        super().__init__(
            _(
                "The page with url {url} couldn't be created, likely due to a page with the same URL already existing.".format(
                    url=url
                )
            )
        )
