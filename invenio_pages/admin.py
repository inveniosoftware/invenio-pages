# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Pages admin interface."""

from __future__ import absolute_import, print_function

import os

from flask import current_app
from flask_admin.contrib.sqla import ModelView
from jinja2 import TemplateNotFound
from werkzeug import secure_filename
from wtforms import TextAreaField
from wtforms.validators import DataRequired, ValidationError

from .models import Page


def template_exists(form, field):
    """Form validation: check that selected template exists."""
    template_name = "invenio_pages/" + secure_filename(field.data)
    try:
        current_app.jinja_env.get_template(template_name)
    except TemplateNotFound:
        raise ValidationError("Template selected does not exist")


class PagesAdmin(ModelView):
    """Page admin."""

    can_create = True
    can_edit = True
    can_delete = True

    create_template = 'pages/edit.html'
    edit_template = 'pages/edit.html'

    column_list = (
        'url', 'title', 'last_modified',
    )
    column_searchable_list = ('url',)

    page_size = 100

    form_args = dict(
        template_name=dict(
            default=lambda: os.path.basename(
                current_app.config["PAGES_DEFAULT_TEMPLATE"]),
            validators=[DataRequired(), template_exists]
        ))

    form_overrides = dict(content=TextAreaField)


pages_adminview = {
    'model': Page,
    'modelview': PagesAdmin,
}
