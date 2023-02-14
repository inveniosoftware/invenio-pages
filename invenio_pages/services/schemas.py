# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pages schema."""

from datetime import timezone

from marshmallow import Schema, fields
from marshmallow_utils.fields import TZDateTime


class PageSchema(Schema):
    """Schema for page."""

    id = fields.String()
    url = fields.String(metadata={"create_only": True})
    title = fields.String()
    content = fields.String()
    description = fields.String()
    template_name = fields.String()
    created = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
    updated = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
