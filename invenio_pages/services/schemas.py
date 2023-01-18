# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pages schema."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import fields


class PageSchema(BaseRecordSchema):
    """Schema for page."""

    id = fields.String()
    url = fields.String()
    title = fields.String()
    content = fields.String()
    description = fields.String()
