# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-License-Identifier: MIT

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
