# SPDX-FileCopyrightText: 2022-2024 CERN.
# SPDX-FileCopyrightText: 2025 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Page Resource Configuration."""

import marshmallow as ma
from invenio_records_resources.resources import (
    RecordResourceConfig,
    SearchRequestArgsSchema,
)


class PageRequestSearchArgs(SearchRequestArgsSchema):
    """Page request search args."""

    sort_direction = ma.fields.Str()


class PageResourceConfig(RecordResourceConfig):
    """Page resource config."""

    # Blueprint configuration
    blueprint_name = "pages"
    url_prefix = "/pages"
    routes = {
        "item": "/<id>",
        "list": "",
    }

    request_search_args = PageRequestSearchArgs
    request_view_args = {
        "id": ma.fields.Integer(),
    }

    response_handlers = {
        "application/vnd.inveniordm.v1+json": RecordResourceConfig.response_handlers[
            "application/json"
        ],
        **RecordResourceConfig.response_handlers,
    }
