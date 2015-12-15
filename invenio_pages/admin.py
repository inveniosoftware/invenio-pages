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

from flask import current_app
from flask_admin.contrib.sqla import ModelView
from jinja2 import TemplateNotFound
from markupsafe import Markup
from werkzeug.local import LocalProxy
from wtforms import IntegerField, SelectField, TextAreaField
from wtforms.validators import ValidationError
from wtforms.widgets import TextArea

from .models import Page, PageList


def _(x):
    """Identity function for string extraction."""
    return x


class CKTextAreaWidget(TextArea):
    """CKEditor widget."""

    def __call__(self, field, **kwargs):
        """Render widget."""
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')  # pragma: no cover
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    """CKEditor field."""

    widget = CKTextAreaWidget()


def template_exists(form, field):
    """Form validation: check that selected template exists."""
    try:
        current_app.jinja_env.get_template(field.data)
    except TemplateNotFound:
        raise ValidationError(_("Template selected does not exist"))


def same_page_choosen(form, field):
    """Check that we are not trying to assign list page itself as a child."""
    if form._obj is not None:
        if field.data.id == form._obj.list_id:
            raise ValidationError(
                _('You cannot assign list page itself as a child.'))


class PagesAdmin(ModelView):
    """Page admin."""

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    create_template = 'invenio_pages/create.html'
    edit_template = 'invenio_pages/edit.html'

    column_list = (
        'url', 'title', 'template_name', 'created', 'updated', 'link')
    column_details_list = (
        'url', 'title', 'template_name', 'description',  'content', 'created',
        'updated', )
    column_filters = (
        'url', 'title', 'template_name', 'content', 'description')
    column_searchable_list = (
        'url', 'title', 'template_name', 'content', 'description')
    column_labels = dict(url='URL')
    column_default_sort = 'url'
    column_formatters = dict(
        link=lambda v, c, m, p: Markup('<a href="{0}">{1}</a>'.format(
            m.url, _('View'))),
        content=lambda v, c, m, p: Markup(m.content),
    )

    page_size = 100

    form_columns = (
        'url', 'title', 'description', 'content', 'template_name', )
    form_args = dict(
        template_name=dict(
            choices=LocalProxy(lambda: current_app.config['PAGES_TEMPLATES'])
        ), )
    form_widget_args = {
        'created': {
            'style': 'pointer-events: none;',
            'readonly': True
        },
        'updated': {
            'style': 'pointer-events: none;',
            'readonly': True
        },
    }
    form_overrides = dict(
        content=CKTextAreaField,
        description=TextAreaField,
        template_name=SelectField,
    )

    inline_models = [
        (PageList, {
            'form_columns': ['id', 'order', 'page'],
            'form_overrides': {'order': IntegerField},
            'form_args': {'page': {'validators': [same_page_choosen]}}
        })
    ]


pages_adminview = {
    'model': Page,
    'modelview': PagesAdmin,
    'category': _('Pages'),
}
