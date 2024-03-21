# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 CERN.
# Copyright (C) 2023 KTH Royal Institute of Technology.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pages schema."""

from datetime import timezone

from flask import current_app
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedHTML, TZDateTime


class DynamicSanitizedHTML(SanitizedHTML):
    """A subclass of SanitizedHTML that dynamically configures allowed HTML tags and attributes based on application settings."""

    def __init__(self, *args, **kwargs):
        """Initializes DynamicSanitizedHTML with dynamic tag and attribute settings."""
        super().__init__(tags=None, attrs=None, *args, **kwargs)

    def _deserialize(self, value, attr, data, **kwargs):
        """Deserialize value with dynamic HTML tags and attributes based on Flask app context or defaults."""
        self.tags = (
            current_app.config.get("ALLOWED_HTML_TAGS", [])
            + current_app.config["PAGES_ALLOWED_EXTRA_HTML_TAGS"]
        )
        self.attrs = self.attrs = dict(
            **current_app.config.get("ALLOWED_HTML_ATTRS", {}),
            **current_app.config["PAGES_ALLOWED_EXTRA_HTML_ATTRS"]
        )

        return super()._deserialize(value, attr, data, **kwargs)


class PageSchema(Schema):
    """Schema for page."""

    id = fields.String()
    url = fields.String(metadata={"create_only": True})
    title = fields.String()
    content = DynamicSanitizedHTML()
    description = fields.String()
    template_name = fields.String()
    created = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
    updated = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
