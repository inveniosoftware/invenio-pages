# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pages permissions."""

from invenio_administration.generators import Administration
from invenio_records_permissions import BasePermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class PagesPermissionPolicy(BasePermissionPolicy):
    """Permission policy for pages."""

    can_create = [SystemProcess()]
    can_read = [AnyUser(), SystemProcess()]
    can_search = [AnyUser(), SystemProcess()]
    can_update = [Administration(), SystemProcess()]
    can_delete = [SystemProcess()]
