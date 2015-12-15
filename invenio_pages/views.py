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

"""Views for Pages module."""

from __future__ import absolute_import, print_function

import six
from flask import Blueprint, abort, current_app, render_template, request
from flask.ctx import after_this_request
from invenio_db import db
from sqlalchemy import event
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound

from .models import Page

blueprint = Blueprint(
    'invenio_pages',
    __name__,
    url_prefix='/',
    template_folder='templates'
)


def preload_pages(original, app, options, first_registration):
    """Register all pages before the first application request."""
    with app.app_context():
        try:
            _add_url_rule([page.url for page in Page.query.all()])
        except Exception:  # pragma: no cover
            current_app.logger.warn('Pages were not loaded.')
            raise
    original(app, options, first_registration=False)

original_register = blueprint.register
blueprint.register = lambda app, options, first_registration=False: \
    preload_pages(original_register, app, options, first_registration)


def view():
    """Public interface to the page view.

    Models: `pages.pages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`pages/default.html` if template_name is not defined.
    Context:
        page
            `pages.pages` object
    """
    return render_page(request.path)


# @cache.memoize for guests?
def render_page(path):
    """Internal interface to the page view."""
    try:
        page = Page.get_by_url(request.path)
    except NoResultFound:
        abort(404)

    return render_template(
        [page.template_name, current_app.config['PAGES_DEFAULT_TEMPLATE']],
        page=page)


def handle_not_found(exception, **extra):
    """Custom blueprint exception handler."""
    assert isinstance(exception, NotFound)

    page = Page.query.filter(db.or_(Page.url == request.path,
                                    Page.url == request.path + "/")).first()

    if page:
        _add_url_rule(page.url)
        return render_template(
            [
                page.template_name,
                current_app.config['PAGES_DEFAULT_TEMPLATE']
            ],
            page=page
        )
    elif 'wrapped' in extra:
        return extra['wrapped'](exception)
    else:
        return exception


def _add_url_rule(url_or_urls):
    """Register URL rule to application URL map."""
    old = current_app._got_first_request
    # This is bit of cheating to overcome @flask.app.setupmethod decorator.
    current_app._got_first_request = False
    if isinstance(url_or_urls, six.string_types):
        url_or_urls = [url_or_urls]
    map(lambda url: current_app.add_url_rule(url, 'invenio_pages.view', view),
        url_or_urls)
    current_app._got_first_request = old
